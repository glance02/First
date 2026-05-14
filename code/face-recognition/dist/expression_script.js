const imageUpload = document.getElementById("upload");
const analysisStage = document.getElementById("analysis-stage");
const expressionResults = document.getElementById("expression-results");
const MODEL_URL = "./models";

const EXPRESSION_LABELS = {
  neutral: "中性",
  happy: "高兴",
  sad: "难过",
  angry: "生气",
  fearful: "害怕",
  disgusted: "厌恶",
  surprised: "惊讶",
};
const EXPRESSION_ORDER = Object.keys(EXPRESSION_LABELS);

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
  faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
]).then(start);

function formatPercent(value) {
  return `${Math.floor(value * 100)}%`;
}

function renderEmptyState(container, title, description) {
  container.innerHTML = `
    <div class="result-empty">
      <strong>${title}</strong>
      <span>${description}</span>
    </div>
  `;
}

function getSortedDetections(detections) {
  return [...detections].sort(
    (first, second) => first.detection.box.x - second.detection.box.x
  );
}

function getTopExpression(expressions) {
  return EXPRESSION_ORDER.reduce(
    (currentTop, key) => {
      const score = expressions[key] || 0;
      return score > currentTop.score ? { key, score } : currentTop;
    },
    { key: EXPRESSION_ORDER[0], score: expressions[EXPRESSION_ORDER[0]] || 0 }
  );
}

function renderExpressionResults(detections) {
  const sortedDetections = getSortedDetections(detections);

  if (!sortedDetections.length) {
    renderEmptyState(
      expressionResults,
      "未检测到人脸",
      "请尝试上传清晰、正脸更明显的照片。"
    );
    return;
  }

  expressionResults.innerHTML = sortedDetections
    .map((detection, index) => {
      const topExpression = getTopExpression(detection.expressions);
      const metrics = EXPRESSION_ORDER.map((key) => {
        const score = detection.expressions[key] || 0;

        return `
          <li class="result-metric">
            <div class="result-metric__row">
              <span class="result-metric__label">${EXPRESSION_LABELS[key]}</span>
              <span class="result-metric__value">${formatPercent(score)}</span>
            </div>
            <div class="result-bar"><span style="width: ${Math.round(
              score * 100
            )}%"></span></div>
          </li>
        `;
      }).join("");

      return `
        <article class="result-card">
          <div class="result-card__header">
            <span class="result-card__title">人脸 ${index + 1}</span>
            <span class="status-pill">${EXPRESSION_LABELS[topExpression.key]}</span>
          </div>
          <p class="result-card__highlight">
            主表情：<strong>${EXPRESSION_LABELS[topExpression.key]}</strong>
            (${formatPercent(topExpression.score)})
          </p>
          <ul class="result-list">${metrics}</ul>
        </article>
      `;
    })
    .join("");
}

async function start() {
  const container = document.createElement("div");
  container.className = "analysis-stage__media";
  analysisStage.append(container);

  let image;
  let canvas;

  imageUpload.addEventListener("change", async () => {
    if (!imageUpload.files.length) {
      return;
    }

    renderEmptyState(expressionResults, "正在识别", "图片分析中，请稍候。");

    if (image) {
      image.remove();
    }
    if (canvas) {
      canvas.remove();
    }

    image = await faceapi.bufferToImage(imageUpload.files[0]);
    container.append(image);

    canvas = faceapi.createCanvasFromMedia(image);
    container.append(canvas);

    const displaySize = { width: image.width, height: image.height };
    faceapi.matchDimensions(canvas, displaySize);

    const detections = await faceapi
      .detectAllFaces(image)
      .withFaceLandmarks()
      .withFaceDescriptors()
      .withFaceExpressions();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
    renderExpressionResults(resizedDetections);

    analysisStage.classList.add("stage-ready");
  });
}
