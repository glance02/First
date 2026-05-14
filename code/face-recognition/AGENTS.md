# 项目基本认知：

这是一个纯前端的人脸分析示例项目，核心依赖是 `face-api.js`，界面层使用 Bootstrap 和 MDB。仓库中没有明显的后端代码，也没有看到 `package.json` 之类的工程化入口；当前形态更接近可直接静态托管的演示站点。

## 主要页面入口：

- `face_recognition.html`：图片上传后做人脸检测与人物识别。
- `face_expression_recognition.html`：图片上传后做人脸表情识别。
- `age_gender_estimation.html`：图片上传后做人脸年龄与性别估计。
- `video_face_tracking.html`：对内置视频 `public/friends.mp4` 做实时人脸检测与表情追踪。
- `webcam_face_tracking.html`：调用摄像头做实时人脸检测、关键点和表情追踪。

## 页面与脚本关系：

- `face_recognition.html` -> `dist/image_script.js`
- `face_expression_recognition.html` -> `dist/expression_script.js`
- `age_gender_estimation.html` -> `dist/estimation_script.js`
- `video_face_tracking.html` -> `dist/video_script.js`
- `webcam_face_tracking.html` -> `dist/webcam_script.js`

## 核心实现特点：

- 每个页面都直接通过 `<script>` 引入 `dist/face-api.min.js` 和对应业务脚本，页面本身很薄，主要逻辑集中在 `dist/*.js`。
- 人脸识别页的已知人物标签固定为《Friends》的 6 个角色：`Chandler`、`Joey`、`Monica`、`Phoebe`、`Rachel`、`Ross`。
- 图片类页面的交互模式基本一致：监听文件上传，创建图片和覆盖层 canvas，然后调用 `face-api.js` 推理并在 canvas 上绘制结果。
- 视频/摄像头页面会在 `video` 播放后创建 canvas，并通过 `setInterval` 持续做人脸检测和结果绘制。

## 模型与资源现状：

- 仓库本地有完整的 `models/` 目录，也有 `public/img/labeled_images/` 训练样本和 `public/friends.mp4`。
- 但当前 `dist/*.js` 加载模型时使用的是 GitHub Raw URL，而不是本地 `models/` 路径。
- `dist/image_script.js` 加载标注人物图片时也使用 GitHub Raw URL，而不是本地 `public/img/labeled_images/`。
- 这意味着当前演示虽然带了本地资源，但运行时仍然依赖外网；如果要做离线运行或提升稳定性，优先检查并改成本地路径。

## 目录理解：

- `dist/`：当前实际被页面直接使用的业务脚本与 `face-api` 构建产物。
- `models/`：`face-api.js` 需要的模型权重文件。
- `public/`：示例图片、角色标注图片、视频等静态资源。
- `css/`、`js/`、`scss/`、`src/`：主要是 Bootstrap、MDB 及其源码/分发文件，属于样式和第三方前端资源层。

修改时的注意点：

- 优先确认变更是落在页面结构还是 `dist/*.js` 逻辑，不要只改 `src/` 或 `scss/` 却忘了当前页面实际引用的是 `dist/` 和现成的 CSS/JS。
- 如果目标是让项目本地可跑、离线可跑或减少外部依赖，优先把模型和标注图片改为从仓库本地路径加载。
- 这是一个结构简单的静态演示项目，改动时应尽量保持直接、可读、低依赖的实现方式。
