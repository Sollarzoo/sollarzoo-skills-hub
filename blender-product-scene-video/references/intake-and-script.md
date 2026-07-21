# Intake and shot-script SOP

## Contents

1. Creative intake
2. Script confirmation
3. Storyboard readiness
4. Environment intake
5. User-help requests
6. Blender handoff checklist

## 1. Creative intake

Inspect supplied files first, then fill only the missing fields.

| Area | Required information | Preferred evidence |
|---|---|---|
| Story | What does each spoken line communicate? | Creative script |
| Product | Which surface or feature must remain readable? | Real screen recording or screenshots |
| Storyboard inputs | Product identity, composition, and style references | Clean product images plus 1–3 references |
| Delivery | Ratio, approximate duration, platform | e.g. 9:16, 30 seconds, social video |
| Constraints | No people, no text, deadline, brand limits | Explicit user statement |

Do not ask for final Blender coordinates, lighting energy, or keyframes during script confirmation.

## 2. Script confirmation

If the script exists, inspect it as the source of truth and verify:

- every spoken line maps to a named scene;
- every clause or meaningful narration fragment maps to one visual beat and primary picture;
- every scene has a clear message and product priority;
- every beat states its emotional intention and design reason;
- every beat defines opening state, primary change, ending state, movement owner, timing, and easing;
- every adjacent beat names whether it is continuous or the exact edit/transition method;
- every required UI image points to a verified screenshot or video timestamp;
- the opening and ending intent are understandable;
- unsupported product behavior is excluded;
- visual boundaries and delivery format are recorded.

If the user has no script, copy `assets/scene-brief-template.md` and use the generic example for structure. Request explicit confirmation before generating the storyboard.

Required beat-sheet columns:

| Field | Requirement |
|---|---|
| Beat id | Stable id such as `SC01-B01` |
| Time | Start/end or bounded target |
| Narration | Exact fragment, not a paraphrase |
| Meaning/emotion | What the viewer should feel or understand |
| Evidence | Screenshot path or recording path plus timestamp/frame |
| Picture | Opening, one primary visual change, ending |
| Motion | Camera/product/UI owner, direction, amount, easing |
| Light | Direction, color intent, reflection behavior, emotional purpose |
| Transition in/out | One-take or named edit method |
| Why | Why this design communicates this fragment |
| Evidence status | `verified / missing / editorial_concept` |

Write a full-film treatment before the table: emotional arc, visual motif, camera language, light/color progression, motion rhythm, transition grammar, physical-phone versus full-screen-UI rules, and opening/ending relationship.

### Product UI evidence gate

Never treat a generated approximation as product evidence. Before storyboarding:

1. inventory available screenshots and recordings;
2. extract representative frames when a video already contains the required UI;
3. attach one evidence path and timestamp/frame to every product beat;
4. list missing captures precisely by screen, state, and required resolution;
5. obtain user confirmation of the refined beat sheet and evidence map.

If a beat is an editorial metaphor, label it on the script and future storyboard. If a beat is a real product claim and evidence is missing, stop.

### UI reference directory contract

Default the project UI evidence root to the `UI参考图/` directory beside the product-video script:

```text
<product-video-project>/UI参考图/
```

The user's exact filename is the canonical UI-state label. For example, `情绪花瓣(周).PNG` means the verified state must be cited as `UI参考图/情绪花瓣(周).PNG`; do not rewrite it as “周花瓣页”, “weekly petals”, or another inferred alias in the evidence field.

Before refining the script:

1. inventory every supported image file in `UI参考图/`;
2. visually inspect every image instead of inferring its contents only from the name;
3. create or refresh `UI参考图/README.md`;
4. record exact relative paths in the beat sheet;
5. distinguish what a still image proves from what requires a continuous recording;
6. list absent UI states as a capture request, using the intended semantic filename.

The evidence index must contain:

| Exact filename | Verified UI state | Supported beats | What this still does not prove |
|---|---|---|---|
| `情绪花瓣(周).PNG` | Weekly emotion-petal view | Exact beat ids | Interaction sequence, if not shown |

Do not rename the supplied files automatically. Do not mix generated crops, annotations, storyboards, or renders into this directory. If a reference screenshot conflicts with a recording, stop the affected beat and ask which represents the current product.

### Phone-axis convention

Use a phone-local coordinate diagram:

- `X_local`: screen left/right;
- `Y_local`: normal to the screen, front/back;
- `Z_local`: phone bottom/top;
- yaw is around `Z_local`;
- pitch is around `X_local`;
- roll is around `Y_local`.

For each rotation, record the axis, signed start/end angles, center/pivot, camera state, and whether screen readability must be preserved. The storyboard must draw the circular path around the actual axis instead of placing an ambiguous loop beside the phone.

## 3. Storyboard readiness

Before generating the Image2 storyboard, collect:

- one or more clean product images or approved renders;
- real UI screenshots or screen-recording frames;
- brand assets that will actually appear;
- one to three composition, lighting, or atmosphere references;
- the previous scene's selected ending frame when continuity matters.

Every product beat must already have a verified reference. “A similar UI probably exists” is not readiness.

For UI screenshots, the storyboard record must cite the exact `UI参考图/<filename>` path. The filename stem remains the visible state name in captions and evidence tables.

Follow `storyboard-sop.md`. Do not open Blender to discover the visual direction.

## 4. Environment intake

Run the Blender MCP preflight only after storyboard approval or when read-only inspection is needed to inventory existing assets. Record:

- Blender location and version;
- Blender MCP server availability;
- Blender Extension state and bridge host/port;
- result of a read-only connection test;
- current `.blend` path;
- whether the user needs to install, enable, restart, log in, or approve anything.

If MCP is unavailable, explain the limitation. Script confirmation and storyboard work may continue; Blender production may not.

## 5. Ask the user for help precisely

Use one compact request at a time:

- “请提供无手机边框、无黑边的原始 MP4/MOV 录屏，保留原始分辨率和帧率。”
- “这是指定型号的手机，需要你提供已授权的 `.blend/.glb/.fbx/.obj` 模型；否则我会使用通用手机造型。”
- “请在 Blender 中启用 MCP 插件并保持 Blender 打开；这一步不需要提供账号或密码。”
- “当前尚未安装 Blender MCP。我可以按官方教程配置服务端和 Blender Extension；需要你批准软件下载，并在 Blender 设置中启用插件。”
- “当前缺少 3D 模型。请在 Sketchfab 登录并下载许可合适的模型，或授权我筛选候选；不要在聊天中提供账号密码。”
- “该素材在私有云盘中，请你完成登录或把文件下载到项目素材目录；不要在聊天中发送密码。”
- “这两种背景会改变影片气质，请确认更偏温暖自然还是冷静科技。”
- “故事版已经展示了手机角度、画面构图和反光方向。请确认这版是否可以作为 Blender 的唯一制作依据。”

No account is needed for Blender, Blender MCP, local image sequences, AVFoundation, or an already installed FFmpeg. A user may need to act for cloud drives, model marketplaces, render farms, paid plugins, or private repositories.

## 6. Blender handoff checklist

Before editing Blender, all creative gates must pass:

- [ ] script explicitly confirmed;
- [ ] spoken-line/scene map confirmed;
- [ ] Image2 storyboard generated from product references and assembled as one numbered grid image;
- [ ] opening, hero, and ending compositions are visible together in chronological grid order;
- [ ] product pose, background, lighting, and reflection intent are annotated;
- [ ] user explicitly approved the selected storyboard direction;
- [ ] storyboard record is marked `approved_for_blender`;
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

Do not infer storyboard approval. If any creative item is unchecked, remain in stage 1 or 2. If the storyboard is approved and only a technical item remains, resolve or ask before the affected Blender operation.
