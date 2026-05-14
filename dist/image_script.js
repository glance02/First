const imageUpload = document.getElementById("upload");
const analysisStage = document.getElementById("analysis-stage");
const MODEL_URL = "./models";
const LABELED_IMAGE_PATH = "./public/img/labeled_images";

Promise.all([
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
]).then(start);

async function start() {
  const container = document.createElement("div");
  container.className = "analysis-stage__media";
  analysisStage.append(container);

  const labeledFaceDescriptors = await loadLabeledImages();
  const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
  let image;
  let canvas;

  imageUpload.addEventListener("change", async () => {
    if (!imageUpload.files.length) {
      return;
    }

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
      .withFaceDescriptors();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    const results = resizedDetections.map((detection) =>
      faceMatcher.findBestMatch(detection.descriptor)
    );

    results.forEach((result, index) => {
      const box = resizedDetections[index].detection.box;
      const drawBox = new faceapi.draw.DrawBox(box, {
        label: result.toString(),
      });
      drawBox.draw(canvas);
    });

    analysisStage.classList.add("stage-ready");
  });
}

function loadLabeledImages() {
  const labels = ["Chandler", "Joey", "Monica", "Phoebe", "Rachel", "Ross"];

  return Promise.all(
    labels.map(async (label) => {
      const descriptions = [];

      for (let i = 1; i <= 5; i += 1) {
        const img = await faceapi.fetchImage(
          `${LABELED_IMAGE_PATH}/${label}/${i}.jpg`
        );
        const detections = await faceapi
          .detectSingleFace(img)
          .withFaceLandmarks()
          .withFaceDescriptor();

        descriptions.push(detections.descriptor);
      }

      return new faceapi.LabeledFaceDescriptors(label, descriptions);
    })
  );
}
