const imageUpload = document.getElementById("upload");
const analysisStage = document.getElementById("analysis-stage");
const estimationResults = document.getElementById("estimation-results");
const MODEL_URL = "./models";

const GENDER_LABELS = {
  male: "男性",
  female: "女性",
};

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.ageGenderNet.loadFromUri(MODEL_URL),
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

function renderEstimationResults(detections) {
  const sortedDetections = getSortedDetections(detections);

  if (!sortedDetections.length) {
    renderEmptyState(
      estimationResults,
      "未检测到人脸",
      "请尝试上传清晰、无遮挡的人像照片。"
    );
    return;
  }

  estimationResults.innerHTML = sortedDetections
    .map((detection, index) => {
      const gender = detection.gender || "male";
      const genderLabel = GENDER_LABELS[gender] || gender;
      const confidence = detection.genderProbability || 0;

      return `
        <article class="result-card">
          <div class="result-card__header">
            <span class="result-card__title">人脸 ${index + 1}</span>
            <span class="status-pill">${genderLabel}</span>
          </div>
          <div class="result-detail-grid">
            <div class="result-detail">
              <span class="result-detail__label">年龄估计</span>
              <span class="result-detail__value">${Math.round(
                detection.age
              )} 岁</span>
            </div>
            <div class="result-detail">
              <span class="result-detail__label">性别判断</span>
              <span class="result-detail__value">${genderLabel}</span>
            </div>
          </div>
          <ul class="result-list">
            <li class="result-metric">
              <div class="result-metric__row">
                <span class="result-metric__label">性别置信度</span>
                <span class="result-metric__value">${formatPercent(
                  confidence
                )}</span>
              </div>
              <div class="result-bar"><span style="width: ${Math.round(
                confidence * 100
              )}%"></span></div>
            </li>
          </ul>
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

    renderEmptyState(estimationResults, "正在识别", "图片分析中，请稍候。");

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
      .withAgeAndGender();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections);

    resizedDetections.forEach((detection, index) => {
      const box = resizedDetections[index].detection.box;
      const drawBox = new faceapi.draw.DrawBox(box, {
        label: `${Math.round(detection.age)} years old ${detection.gender}`,
      });
      drawBox.draw(canvas);
    });

    renderEstimationResults(resizedDetections);

    analysisStage.classList.add("stage-ready");
  });
}
