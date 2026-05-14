const video = document.getElementById("video");
const trackingStage = document.getElementById("tracking-stage");
const webcamStatus = document.getElementById("webcam-status");
const webcamResults = document.getElementById("webcam-results");
const MODEL_URL = "./models";
let canvas;
let detectionInterval;
let lastResultsMarkup = "";
let lastResultsRenderAt = 0;

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
const SIDEBAR_REFRESH_MS = 280;

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
]).then(startVideo);

function getDisplaySize() {
  return {
    width: Math.max(trackingStage.clientWidth, 1),
    height: Math.max(trackingStage.clientHeight, 1),
  };
}

function syncCanvasSize() {
  if (!canvas) {
    return getDisplaySize();
  }

  const displaySize = getDisplaySize();

  if (canvas.width !== displaySize.width || canvas.height !== displaySize.height) {
    faceapi.matchDimensions(canvas, displaySize);
  }

  return displaySize;
}

function formatPercent(value) {
  return `${Math.floor(value * 100)}%`;
}

function renderStatus(title, badge, description) {
  webcamStatus.innerHTML = `
    <div class="result-card result-card--status">
      <div class="result-card__header">
        <span class="result-card__title">${title}</span>
        <span class="status-pill">${badge}</span>
      </div>
      <p class="result-card__meta">${description}</p>
    </div>
  `;
}

function renderEmptyResults(title, description, force = false) {
  lastResultsMarkup = "";
  webcamResults.innerHTML = `
    <div class="result-empty">
      <strong>${title}</strong>
      <span>${description}</span>
    </div>
  `;

  if (force) {
    lastResultsRenderAt = 0;
  }
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

function buildResultsMarkup(detections) {
  const sortedDetections = getSortedDetections(detections);

  if (!sortedDetections.length) {
    return `
      <div class="result-empty">
        <strong>未检测到人脸</strong>
        <span>当前画面中还没有检测到清晰人脸。</span>
      </div>
    `;
  }

  return sortedDetections
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

function renderWebcamResults(detections, force = false) {
  const markup = buildResultsMarkup(detections);
  const now = Date.now();

  if (!force && markup === lastResultsMarkup) {
    return;
  }

  if (!force && now - lastResultsRenderAt < SIDEBAR_REFRESH_MS) {
    return;
  }

  webcamResults.innerHTML = markup;
  lastResultsMarkup = markup;
  lastResultsRenderAt = now;
}

function startVideo() {
  renderStatus("等待授权", "未连接", "允许浏览器访问摄像头后开始实时识别。");
  renderEmptyResults(
    "等待识别",
    "摄像头开始工作后，这里会同步显示表情识别结果副本。",
    true
  );

  const legacyGetUserMedia =
    navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia;

  const getUserMedia =
    navigator.mediaDevices && navigator.mediaDevices.getUserMedia
      ? (constraints) => navigator.mediaDevices.getUserMedia(constraints)
      : legacyGetUserMedia
      ? (constraints) =>
          new Promise((resolve, reject) => {
            legacyGetUserMedia.call(navigator, constraints, resolve, reject);
          })
      : null;

  if (!getUserMedia) {
    console.error("Camera API is not supported in this browser.");
    renderStatus("摄像头不可用", "不支持", "当前浏览器不支持摄像头访问接口。");
    renderEmptyResults(
      "无法开始识别",
      "请更换支持摄像头访问的浏览器后重试。",
      true
    );
    return;
  }

  renderStatus("正在连接", "连接中", "正在请求摄像头权限，请稍候。");

  getUserMedia({ video: {} })
    .then((stream) => {
      video.srcObject = stream;
      renderStatus("摄像头已连接", "已连接", "画面已连接，等待浏览器开始播放视频流。");
    })
    .catch((error) => {
      console.error(error);
      renderStatus(
        "访问失败",
        "不可用",
        "未能获取摄像头权限，或者当前设备不可用。"
      );
      renderEmptyResults(
        "无法开始识别",
        "请检查浏览器授权和摄像头设备后重试。",
        true
      );
    });
}

video.addEventListener("play", () => {
  if (!canvas) {
    canvas = faceapi.createCanvasFromMedia(video);
    trackingStage.append(canvas);
  }

  syncCanvasSize();
  trackingStage.classList.add("stage-live");
  renderStatus("正在识别", "识别中", "已连接摄像头，正在同步更新实时识别结果。");

  window.clearInterval(detectionInterval);
  detectionInterval = window.setInterval(async () => {
    const displaySize = syncCanvasSize();
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
    renderWebcamResults(resizedDetections);
  }, 100);
});

window.addEventListener("resize", () => {
  syncCanvasSize();
});

["pause", "ended"].forEach((eventName) => {
  video.addEventListener(eventName, () => {
    window.clearInterval(detectionInterval);
    renderStatus("识别已暂停", "已暂停", "摄像头画面已暂停，左侧结果已停止更新。");
    renderEmptyResults(
      "识别已暂停",
      "恢复摄像头画面后，这里会重新同步显示识别结果。",
      true
    );
  });
});
