# Intake and shot-script SOP

## Contents

1. Environment intake
2. Minimum creative intake
3. User-help requests
4. Script drafting
5. Shot decision rules
6. Approval checklist

## 1. Environment intake

Run the Blender MCP preflight in `blender-mcp-setup.md` before creative intake. Record:

- Blender location and version;
- Blender MCP server availability;
- Blender Extension state and bridge host/port;
- result of a read-only connection test;
- current `.blend` path;
- whether the user needs to install, enable, restart, log in, or approve anything.

If MCP is unavailable, explain the limitation and continue only with script/assets or the documented background/script fallback.

## 2. Minimum creative intake

Inspect supplied files first, then fill only the missing fields.

| Area | Required information | Preferred evidence |
|---|---|---|
| Story | What changes from the first frame to the last? | Creative script or storyboard |
| Product | Which surface or feature must remain readable? | Real screen recording or screenshots |
| Model | Generic or named device; visible angles | `.blend`, `.glb`, `.fbx`, `.obj` |
| Materials | Finish, color, glass, metal, roughness | PBR maps and reference photos |
| Motion | Camera move, product move, or hybrid | Timing notes and event frames |
| Style | Warm/cool, background, contrast, realism | 1–3 reference images |
| Delivery | Ratio, pixels, fps, duration, platform | e.g. 9:16, 1080×1920, 30fps |
| Constraints | No text, no people, deadline, render budget | Explicit user statement |

Do not ask again for information already present in the conversation, script, scene, or asset folder.

## 3. Ask the user for help precisely

Use one compact request at a time:

- “请提供无手机边框、无黑边的原始 MP4/MOV 录屏，保留原始分辨率和帧率。”
- “这是指定型号的手机，需要你提供已授权的 `.blend/.glb/.fbx/.obj` 模型；否则我会使用通用手机造型。”
- “请在 Blender 中启用 MCP 插件并保持 Blender 打开；这一步不需要提供账号或密码。”
- “当前尚未安装 Blender MCP。我可以按官方教程配置服务端和 Blender Extension；需要你批准软件下载，并在 Blender 设置中启用插件。”
- “当前缺少 3D 模型。请在 Sketchfab 登录并下载许可合适的模型，或授权我筛选候选；不要在聊天中提供账号密码。”
- “该素材在私有云盘中，请你完成登录或把文件下载到项目素材目录；不要在聊天中发送密码。”
- “这两种背景会改变影片气质，请确认更偏温暖自然还是冷静科技。”

No account is needed for Blender, Blender MCP, local image sequences, AVFoundation, or an already installed FFmpeg. A user may need to act for cloud drives, model marketplaces, render farms, paid plugins, or private repositories.

## 4. Draft a missing script

Copy `assets/scene-brief-template.md`. Convert qualitative wishes into measurable instructions.

Bad:

> 镜头慢慢拉远，背景高级一点。

Good:

> 第 1–360 帧聚焦屏幕下方输入框；第 361–781 帧手机沿世界 Y 轴后退，相机只承担约 20% 的后移；第 781 帧发送完成时到达完整手机机位并停止。背景墙固定，仅 Shader 缓慢流动。

The shot specification must include:

- frame range and seconds;
- first, middle, stop, and final states;
- camera lens, pose, target, and movement;
- product rig pose and movement;
- focus object and aperture;
- screen-video timing;
- lighting direction and roles;
- background geometry and Shader behavior;
- output settings;
- acceptance criteria.

When the screen video defines story timing, inspect its real duration and identify event frames. Do not guess when typing ends, a send action occurs, or a feature transition begins.

## 5. Choose camera, product, or hybrid motion

- Move the camera when the environment should reveal parallax and the subject can remain spatially fixed.
- Move the product when the background should feel stable and the product must change scale strongly.
- Use hybrid motion when a frontal push/pull makes foreground and background feel glued together. Let the product carry most depth change and the camera supply subtle reframing.
- Keep background geometry fixed unless the story explicitly calls for a moving set. Animate its material coordinates for slow light flow.

Do not animate both camera and product with equal, unmotivated movement. Assign a clear movement owner.

## 6. Approval checklist

Before editing Blender, confirm or infer safely:

- [ ] Blender MCP read-only connection succeeds;
- [ ] returned `.blend` path is correct;
- [ ] real product feature shown;
- [ ] first and last composition;
- [ ] movement owner and stop event;
- [ ] delivery ratio/resolution/fps;
- [ ] background and lighting direction;
- [ ] subtitles/audio policy;
- [ ] source assets and licenses;
- [ ] preview-versus-final quality budget.

If any unchecked item would materially alter the creative result, ask. Otherwise proceed and state the assumption.
