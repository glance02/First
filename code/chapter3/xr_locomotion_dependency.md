# Fantasy Forest 场景中的 VR 移动逻辑依赖分析

## 1. 场景移动逻辑来源

`Assets/Fantasy Forest Environment Free Sample` 资源包本身主要提供森林环境、地形、模型、材质和样例场景。该资源包内部并没有实现键盘移动、第一人称移动或 VR 移动的脚本。

当前森林样例场景中的移动能力来自项目中已经配置好的 XR Rig。也就是说，森林场景只是作为环境载体，真正的移动逻辑由 Unity XR Interaction Toolkit、XR Origin 预制体、Input Actions 和 Locomotion Provider 共同实现。

依赖链如下：

```text
Fantasy Forest demoScene_free.unity
    -> Complete XR Origin Set Up Hands Variant.prefab
        -> XR Origin Hands (XR Rig).prefab
            -> XRI Default Input Actions.inputactions
            -> ControllerInputActionManager.cs
            -> DynamicMoveProvider.cs
            -> XR Interaction Toolkit Locomotion Runtime
```

## 2. 关键依赖文件

### 2.1 场景文件

```text
Assets/Fantasy Forest Environment Free Sample/Scenes/demoScene_free.unity
```

该场景中放置了 `XR Origin Hands (XR Rig)`，用于提供 VR 视角、手部交互、控制器输入和移动能力。原森林资源包中的普通 Camera 只负责场景预览，不包含 VR 移动逻辑。

### 2.2 XR Origin 预制体

```text
Assets/VRTemplateAssets/Prefabs/Setup/Complete XR Origin Set Up Hands Variant.prefab
```

该预制体是森林场景中实际使用的 XR Rig 变体。它包含完整的 VR Origin 设置，包括主相机、Camera Offset、手部控制器、移动组件和相关输入引用。

```text
Assets/Samples/XR Interaction Toolkit/3.4.1/Hands Interaction Demo/Prefabs/XR Origin Hands (XR Rig).prefab
```

该预制体是 Hands Demo 中的 XR Origin 基础版本，`Complete XR Origin Set Up Hands Variant.prefab` 是基于它构建出来的变体。

### 2.3 输入动作配置

```text
Assets/Samples/XR Interaction Toolkit/3.4.1/Starter Assets/XRI Default Input Actions.inputactions
```

该文件定义了 XR 控制器输入动作，包括：

- `XRI Left Locomotion`
- `XRI Right Locomotion`
- `Move`
- `Turn`
- `Snap Turn`
- `Teleport Mode`
- `Teleport Mode Cancel`

其中 `Move` 负责连续移动输入，`Turn` 和 `Snap Turn` 负责旋转，`Teleport Mode` 负责启用传送射线。

### 2.4 输入动作管理脚本

```text
Assets/Samples/XR Interaction Toolkit/3.4.1/Starter Assets/Scripts/ControllerInputActionManager.cs
```

该脚本负责管理控制器上的移动、转向、传送和 UI 滚动输入。它会根据当前移动模式启用或禁用不同的输入动作，避免移动、传送、物体操作和 UI 操作互相冲突。

### 2.5 连续移动脚本

```text
Assets/Samples/XR Interaction Toolkit/3.4.1/Starter Assets/Scripts/DynamicMoveProvider.cs
```

该脚本继承自 XR Interaction Toolkit 的 `ContinuousMoveProvider`。它根据头显方向或手柄方向决定玩家移动的参考方向，再把输入交给基础移动逻辑处理。

## 3. 报告中建议展示的代码

报告中不建议完整展示 `.prefab` 或 `.unity` 文件，因为它们是 Unity 序列化生成的 YAML 文件，内容很长，可读性较差。更适合展示的是输入绑定脚本和移动处理脚本。

建议展示以下三段代码。

### 3.1 输入动作引用

文件：

```text
ControllerInputActionManager.cs
```

推荐展示：

```csharp
InputActionReference m_TeleportMode;
InputActionReference m_TeleportModeCancel;
InputActionReference m_Turn;
InputActionReference m_SnapTurn;
InputActionReference m_Move;
InputActionReference m_UIScroll;
```

这段代码说明移动、转向、传送和 UI 滚动并不是写死在脚本中的，而是通过 `InputActionReference` 引用 `.inputactions` 文件中配置好的动作。

### 3.2 移动模式切换逻辑

文件：

```text
ControllerInputActionManager.cs
```

推荐展示：

```csharp
void UpdateLocomotionActions()
{
    SetEnabled(m_Move, m_SmoothMotionEnabled);
    SetEnabled(m_TeleportMode, !m_SmoothMotionEnabled);
    SetEnabled(m_TeleportModeCancel, !m_SmoothMotionEnabled);

    SetEnabled(m_Turn, !m_SmoothMotionEnabled && m_SmoothTurnEnabled);
    SetEnabled(m_SnapTurn, !m_SmoothMotionEnabled && !m_SmoothTurnEnabled);
}
```

这段代码体现了系统如何在“连续移动”和“传送移动”之间切换：

- 当 `m_SmoothMotionEnabled` 为 true 时，启用 `Move`，使用摇杆连续移动。
- 当 `m_SmoothMotionEnabled` 为 false 时，禁用连续移动，启用传送模式。
- 转向也分为连续转向 `Turn` 和瞬间转向 `Snap Turn`。

### 3.3 连续移动方向计算

文件：

```text
DynamicMoveProvider.cs
```

推荐展示：

```csharp
var leftHandValue = leftHandMoveInput.ReadValue();
var rightHandValue = rightHandMoveInput.ReadValue();

var totalSqrMagnitude = leftHandValue.sqrMagnitude + rightHandValue.sqrMagnitude;
var leftHandBlend = 0.5f;
if (totalSqrMagnitude > Mathf.Epsilon)
    leftHandBlend = leftHandValue.sqrMagnitude / totalSqrMagnitude;

var combinedPosition = Vector3.Lerp(m_RightMovementPose.position, m_LeftMovementPose.position, leftHandBlend);
var combinedRotation = Quaternion.Slerp(m_RightMovementPose.rotation, m_LeftMovementPose.rotation, leftHandBlend);
m_CombinedTransform.SetPositionAndRotation(combinedPosition, combinedRotation);

return base.ComputeDesiredMove(input);
```

这段代码说明移动方向不是固定世界坐标方向，而是会根据左右手输入强度，在左右手或头显参考方向之间进行混合。最后调用 `base.ComputeDesiredMove(input)`，交给 XR Interaction Toolkit 的连续移动基础逻辑计算实际位移。

## 4. 代码附件

本章节需要展示或引用的代码文件已经复制到：

```text
code/chapter3
```

包含文件：

```text
code/chapter3/DynamicMoveProvider.cs
code/chapter3/ControllerInputActionManager.cs
code/chapter3/XRI Default Input Actions.inputactions
```

其中：

- `DynamicMoveProvider.cs` 用于展示连续移动方向计算。
- `ControllerInputActionManager.cs` 用于展示输入动作管理和移动模式切换。
- `XRI Default Input Actions.inputactions` 用于展示 XR 控制器输入动作配置。

## 5. 小结

森林场景中的移动系统并不是资源包自带的脚本实现，而是依赖 Unity XR Interaction Toolkit 的标准移动框架。整体流程可以概括为：

```text
手柄摇杆/按钮输入
    -> XRI Default Input Actions
        -> ControllerInputActionManager 启用对应输入动作
            -> DynamicMoveProvider 计算移动方向
                -> ContinuousMoveProvider 执行实际移动
                    -> XR Origin 在森林场景中移动
```

因此，在报告中说明森林场景移动逻辑时，重点应放在 XR Origin 的依赖链、Input Actions 的绑定关系，以及 `ControllerInputActionManager` 和 `DynamicMoveProvider` 两个脚本的作用。
