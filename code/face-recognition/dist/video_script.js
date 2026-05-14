const video = document.getElementById("video");
const trackingStage = document.getElementById("tracking-stage");
const MODEL_URL = "./models";
let canvas;
let detectionInterval;

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
]).then(startVideo);

function startVideo() {
  video.addEventListener("play", () => {
    if (!canvas) {
      canvas = faceapi.createCanvasFromMedia(video);
      trackingStage.append(canvas);
    }

    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);
    trackingStage.classList.add("stage-live");

    window.clearInterval(detectionInterval);
    detectionInterval = window.setInterval(async () => {
      const detections = await faceapi
        .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceExpressions();

      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
    }, 120);
  });

  ["pause", "ended"].forEach((eventName) => {
    video.addEventListener(eventName, () => {
      window.clearInterval(detectionInterval);
    });
  });
}
