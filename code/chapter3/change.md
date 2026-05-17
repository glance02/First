# Unity 项目问题与修改记录

## 项目信息确认

### 遇到的问题

需要确认当前 Unity 项目的版本，以及使用的渲染管线，方便判断导入资源包是否兼容。

### 确认结果

- Unity 版本：`6000.3.14f1`
- 渲染管线：`Universal Render Pipeline`
- URP 包版本：`17.3.0`

### 判断依据

- Unity 版本来自：`ProjectSettings/ProjectVersion.txt`
- URP 包版本来自：`Packages/manifest.json`
- 当前项目渲染管线配置来自：`ProjectSettings/GraphicsSettings.asset`
- 当前使用的 URP 配置资产：`Assets/Settings/Project Configuration/Performance URP Config.asset`

## Fantasy Forest Environment Free Sample 导入后全粉

### 遇到的问题

导入资源包：

`Assets/Fantasy Forest Environment Free Sample`

打开资源包样例场景后，模型和材质大面积显示为粉色。

### 原因分析

这个资源包要求的 Unity 版本是 `2021.3.9f1`，资源本身主要面向旧的 Built-in Render Pipeline。

当前项目使用的是 Unity 6 + URP 17.3.0。Unity 中材质显示为粉色通常表示当前材质引用的 shader 无法在当前渲染管线中正常编译或使用。

检查后发现：

- `dirt01.mat`、`grass01.mat` 等材质仍引用旧的内置 shader。
- `grassmesh.mat`、`tree_branches.mat` 引用了资源包自带 shader：`Fantasy Forest/StandardNoCulling`。
- 原始 `StandardNoCulling.shader` 使用了 Built-in 管线的 Surface Shader 写法，例如 `#pragma surface surf StandardSpecular ...`。
- URP 不支持 Built-in Surface Shader，所以这些材质在当前项目里会变粉。

### 解决方案

将资源包自带的 `StandardNoCulling.shader` 改写为 URP 可用的 HLSL shader，并让相关材质统一引用这个兼容版本。

### 修改的代码文件

代码较多，文件地址如下：

`Assets/Fantasy Forest Environment Free Sample/StandardNoCulling.shader`

主要修改内容：

- 将旧 Built-in Surface Shader 替换为 URP HLSL shader。
- 增加 `UniversalForward` pass，用于正常渲染。
- 增加 `ShadowCaster` pass，用于阴影。
- 保留原资源需要的贴图 `_MainTex`、颜色 `_Color`、透明裁剪 `_Cutoff`、光滑度 `_Glossiness` 属性。
- 保留双面显示逻辑：`Cull Off`，用于草、树叶等资源。
- 透明裁剪使用贴图 alpha，避免原资源中 `_Color.a = 0` 的树叶材质被错误裁掉。

### 修改的材质文件

这些材质原本引用旧 shader，现在改为引用新的 `Fantasy Forest/StandardNoCulling`：

- `Assets/Fantasy Forest Environment Free Sample/Materials/dirt01.mat`
- `Assets/Fantasy Forest Environment Free Sample/Materials/grass01.mat`
- `Assets/Fantasy Forest Environment Free Sample/Materials/bark01_bottom.mat`

这些材质原本已经引用 `Fantasy Forest/StandardNoCulling`，因此会自动使用修复后的 URP shader：

- `Assets/Fantasy Forest Environment Free Sample/Materials/grassmesh.mat`
- `Assets/Fantasy Forest Environment Free Sample/Materials/tree_branches.mat`

### 验证结果

- Unity 脚本重新编译通过。
- Unity Console 没有 shader 或编译错误。
- 材质可识别到 `Shader: Fantasy Forest/StandardNoCulling`。
- `grassmesh`、`tree_branches`、`dirt01`、`bark01_bottom` 等材质能解析出 shader pass。

## 是否可以通过安装旧 Unity 解决

### 问题说明

资源包说明需要 `Unity 2021.3.9f1`，因此询问是否下载旧 Unity 就可以使用。

### 结论

如果新建一个 `Unity 2021.3.9f1` 的 Built-in Render Pipeline 项目，这个资源包大概率可以正常显示。

但是当前项目是 `Unity 6000.3.14f1`，不建议把当前项目降级到 Unity 2021，因为 Unity 项目通常不支持安全地从高版本降到低版本，尤其当前项目还包含 URP、XR、Input System 等依赖。

更合适的做法是继续在当前 Unity 6 + URP 项目中修复资源包的 shader 和材质。

## 将 SampleScene 的 VR 视角复制到森林场景

### 遇到的问题

当前项目的 `SampleScene` 里已经有可用的 VR 视角，希望把这个 VR 视角复制到修复后的森林样例场景里。

源场景：

`Assets/Scenes/SampleScene.unity`

目标场景：

`Assets/Fantasy Forest Environment Free Sample/Scenes/demoScene_free.unity`

### 解决方案

没有只复制单独的 Camera，而是复制完整的 XR Origin 预制体。这样可以保留 VR 相机、手部、控制器、输入、移动相关组件。

使用的预制体：

`Assets/VRTemplateAssets/Prefabs/Setup/Complete XR Origin Set Up Hands Variant.prefab`

### 场景修改内容

在森林场景中新增：

`XR Origin Hands (XR Rig)`

位置设置为参考森林场景原普通相机的位置：

- X：`17.5541019`
- Y：`0`
- Z：`28.302784`

朝向参考原普通相机的水平朝向：

- Y Rotation：`350.638153`

同时关闭森林场景原来的普通 `Camera`，避免它和 XR Rig 内部的 `Main Camera` 同时渲染或抢占主相机。

修改后的场景文件：

`Assets/Fantasy Forest Environment Free Sample/Scenes/demoScene_free.unity`

### 验证结果

- `demoScene_free.unity` 已保存。
- 场景中存在 `XR Origin Hands (XR Rig)`。
- XR Rig 内部包含 `Main Camera`、`Camera Offset`、手部、控制器、输入和移动相关组件。
- 原普通 `Camera` 已设为 inactive。
- Unity Console 当前没有错误。

## 后续注意事项

- 如果打开森林场景后仍有个别材质显示异常，可以继续检查对应材质是否还在引用旧 Built-in shader。
- 如果 VR 出生点位置、方向或高度不舒服，可以继续调整 `XR Origin Hands (XR Rig)` 的 Transform。
- 森林场景中的地形已有 `TerrainCollider`，VR 玩家移动和重力检测可以正常依赖地形碰撞。

## 报告中建议展示的代码文件

如果后续需要把本次修改的代码贴进报告，最建议展示这个文件：

`Assets/Fantasy Forest Environment Free Sample/StandardNoCulling.shader`

原因：

- 这是本次真正进行代码级修复的文件。
- 它直接解决了旧资源包导入 Unity 6 + URP 后材质变粉的问题。
- 修改内容能清楚体现问题原因和解决思路：将旧 Built-in Surface Shader 改写为 URP 可用的 HLSL shader。

报告中可以重点说明：

- 原资源包使用 Built-in Render Pipeline 的 Surface Shader。
- 当前项目使用 URP，旧 shader 无法正常编译或渲染，所以材质显示为粉色。
- 通过重写 `StandardNoCulling.shader`，增加 `UniversalForward` 和 `ShadowCaster` pass，使草、树叶、树干、地面等材质恢复正常显示。
- 保留了原资源需要的双面渲染和透明裁剪逻辑，保证草和树叶不会显示异常。

不建议在报告中完整粘贴这些文件：

- `.mat` 材质文件：只是修改 shader 引用，适合列路径，不适合贴完整内容。
- `demoScene_free.unity`：场景 YAML 文件很长，只需要说明新增了 `XR Origin Hands (XR Rig)` 并关闭原普通相机。
- `change.md`：这是过程记录文档，可以作为说明依据，但不是核心代码。
