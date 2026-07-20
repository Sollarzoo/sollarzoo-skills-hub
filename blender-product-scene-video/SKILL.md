---
name: blender-product-scene-video
description: Build and deliver reusable Blender product-scene animations from a creative script, 3D model, textures, screen recording, and visual references. Use when Codex needs to verify or configure Blender MCP, obtain a properly licensed model, inspect or initialize a Blender scene, write a missing shot script, load and position a product model, configure PBR materials and video textures, design lighting/background/procedural Shader animation, animate cameras or products, render reviewed image sequences, encode final MP4 video, diagnose flicker/blur/framing/render-time problems, or document the production settings for later scenes.
---

# Blender Product Scene Video

## Skill metadata

- Author: [sollarzoo](https://github.com/Sollarzoo)
- Version: `1.2.6`
- Feedback WeChat: `sollarzoo`

## Outcome

Turn a product-film idea into four synchronized deliverables:

1. an approved shot specification;
2. a reversible `.blend` scene;
3. a complete, validated image sequence;
4. a playable final video plus thumbnail and production record.

Keep real product UI legible. Do not invent product behavior that the supplied recording does not show.

## Load the relevant resources

- Read [references/blender-mcp-setup.md](references/blender-mcp-setup.md) at the start of every new machine or when Blender tools are unavailable.
- Read [references/intake-and-script.md](references/intake-and-script.md) before drafting or changing the shot.
- Read [references/scene-build-sop.md](references/scene-build-sop.md) before modifying Blender.
- Read [references/render-export-qc.md](references/render-export-qc.md) before a full export.
- Read [references/troubleshooting.md](references/troubleshooting.md) when diagnosing flicker, blur, wrong speed, weak lighting, framing, or slow rendering.
- Read [references/generic-product-film-script-example.md](references/generic-product-film-script-example.md) when the user has no full production script or wants a complete, business-neutral example of the script structure.
- Copy [assets/scene-brief-template.md](assets/scene-brief-template.md) when the user has no usable shot script.

## Apply the interaction contract

Start with a concise commentary update. State which source files and scene will be inspected. Never modify an unfamiliar scene before inspecting its collections, objects, materials, lights, camera, animation, render settings, units, visibility, and active file path.

Ask the user only when the answer materially changes the creative result, requires credentials, or authorizes a risky external action.

### Keep progress visible

Map the internal workflow to these seven user-facing phases:

1. Blender and MCP preflight;
2. source assets and shot specification;
3. scene setup and controlled build;
4. still-frame review through gates A–C;
5. short motion proof through gate D;
6. image-sequence render, validation, encoding, and QC;
7. script synchronization and complete handoff.

At the start, after every phase transition, before requesting approval, whenever work pauses or becomes blocked, and at final handoff, publish a compact status block in the user's language:

```text
Progress: phase 4/7 — Still-frame review
Completed: SC02 copy, camera animation, look target, and focus target
Current: checking opening, middle, stop, and final frames
Next: render a short motion proof
Then: export the image sequence after approval
User action: none
```

Apply these rules:

- put only verified outcomes under `Completed`;
- name exactly one immediate action under `Next` and one following action under `Then`;
- write `User action: none` when the user does not need to intervene;
- when entering an existing project midway, mark earlier phases as completed, skipped, or not applicable instead of pretending to restart;
- distinguish technical preview, approval gate, production render, validation, encoding, and final delivery;
- do not use vague updates such as “still working” without stating the current phase and next checkpoint.

During a render or another operation expected to take longer than about one minute, add measurable sub-progress:

```text
Render: 48/150 frames
Elapsed: about 2 minutes
Estimated remaining: about 4 minutes
After render: validate frame count and inspect representative frames
```

Use actual frame counts and status files when available. If a reliable estimate is unavailable, say so instead of inventing one. Update the user at meaningful milestones and at least about once per minute while the operation is active.

When paused for approval or blocked by a missing asset, connection, or permission, state the exact gate, what is already safe and complete, the decision or input required, and what resumes immediately afterward.

### Require user input for

- the intended story, visual references, product priority, aspect ratio, duration, and delivery platform when they cannot be inferred;
- approval of a newly written shot specification;
- a missing screen recording, licensed/named product model, brand asset, font, or private cloud file;
- login, OAuth, paid asset purchase, plugin installation, or any external account action;
- destructive replacement of an existing scene, render sequence, or final video;
- the visual direction when two plausible options would create materially different scenes.

Tell the user exactly what to provide: supported file type, preferred resolution/frame rate, whether borders or device frames must be removed, and where the file should be placed. Never request passwords or tokens in chat. Ask the user to complete login in the relevant application.

### Proceed autonomously for

- read-only inspection and inventory;
- backups, collections, naming, parenting, material node cleanup, color-space corrections, and reversible modifiers;
- low-resolution preview renders and technical QC;
- adjustments that implement an already approved direction;
- image-sequence validation and local video encoding;
- documentation of final coordinates, frames, lighting, Shader parameters, and output paths.

Report meaningful changes using the progress contract above.

## Execute the workflow

### 0. Run the Blender MCP preflight

Before inspecting assets or promising Blender execution:

1. check whether Blender is installed and record its version;
2. search for callable Blender MCP tools;
3. call a read-only path/scene-summary tool to verify the live connection;
4. confirm the returned `.blend` is the file the user intends to edit.

If any check fails, follow [references/blender-mcp-setup.md](references/blender-mcp-setup.md). Do not treat “tool listed” as “Blender connected.” A successful read-only call is the connection gate.

Installing Blender, downloading the MCP components, editing a global MCP configuration, or installing/enabling the Blender extension requires an explicit user-facing explanation and any approval required by the host. The user must complete interactive login or OS prompts. Never request credentials in chat.

If MCP cannot be configured now, use the documented fallback: inspect files and prepare the shot specification or Blender Python script, but do not claim live scene changes. Use background Blender only for operations that do not require an interactive viewport.

### 1. Establish the source of truth

Collect the creative script, model, textures, screen recording, references, output ratio, resolution, frame rate, duration, and destination platform. Inspect exact files rather than relying on filenames or old notes.

If the user has no script, read the generic product-film script example, copy the scene brief template, draft a measurable shot specification, and ask for approval before building. Use the example only for structure; replace all placeholders with verified project facts. A usable specification names the subject, opening frame, end frame, movement owner, key timing events, focus target, background behavior, lighting direction, duration, and output settings.

If the user has no model, search the user-approved source such as [Sketchfab](https://sketchfab.com/3d-models). Ask the user to log in or purchase the asset when required. Download only models explicitly marked downloadable and compatible with the intended use. Record creator, source URL, license, and any attribution requirement.

### 2. Decide the production route

- Use true Blender 3D for visible thickness, side/rear views, glass/metal reflections, strong parallax, or physically meaningful lighting.
- Use flat compositing only when the phone remains nearly frontal and no convincing thickness is needed.
- For uncertain geometry or realism, create a 3–5 second proof before committing to the full animation.

### 3. Initialize safely

Create a scene workspace with:

```bash
python3 scripts/init_project.py <project-dir> --name <scene-slug>
```

Use the generated directories for source assets, previews, image sequences, videos, and logs. Keep source assets immutable. Save a timestamped or purpose-named `.blend` backup before every structural change.

### 4. Build in controlled passes

Follow [references/scene-build-sop.md](references/scene-build-sop.md) in this order:

1. model and scale;
2. UVs and materials;
3. screen/video texture;
4. product pose and camera;
5. product lighting;
6. physical background and Shader;
7. animation rigs and focus;
8. render optimization.

Use stable names such as `SC##_ProductRig`, `SC##_CameraRig`, `SC##_LookTarget`, `SC##_ScreenFocus`, `SC##_Physical_BackWall`, and role-based light names. Prefer 5–8 purposeful lights. Add more only when each has a visible, documented job.

### 5. Use confirmation gates

Render small previews before expensive work:

- gate A: model, screen UV, and framing;
- gate B: material, glass reflection, and lighting;
- gate C: opening, middle, stop, and final animation frames;
- gate D: short motion proof at delivery aspect ratio.

Show the user representative images and describe what changed. Ask for approval only at a creative fork or before the full export. Technical defects found during the gates should be fixed without asking.

### 6. Export images first

For every production animation, export a numbered JPEG, PNG, or EXR sequence before making a movie. This is the default recovery contract, not an optional optimization: it preserves completed frames after interruption, permits single-frame repair, and enables re-encoding without re-rendering Blender.

Allow direct-to-video output only for a disposable 1–3 second technical preview when all of these are true:

- the user does not need resumability or frame-level repair;
- no alpha, grading intermediate, or later codec change is required;
- rerendering the entire preview would be trivial.

Static-image scenes do not need video encoding. Screen capture and live-stream workflows are outside this image-sequence rule and must be identified explicitly.

For fast review, use rendered-viewport export. For hero/final quality, use Eevee or Cycles according to the approved quality/time budget. Never silently lower resolution, frame rate, duration, or playback speed.

Validate the sequence:

```bash
python3 scripts/validate_image_sequence.py <frames-dir> \
  --expected-count <count> --width <width> --height <height>
```

### 7. Encode and verify

Detect the operating system before selecting the encoder.

On macOS, prefer the bundled AVFoundation encoder; FFmpeg is optional. Compile the encoder once:

```bash
xcrun swiftc -O scripts/encode_avfoundation.swift \
  -o scripts/encode_avfoundation
```

Then encode:

```bash
scripts/encode_avfoundation <frames-dir> <output.mp4> <thumbnail.jpg> \
  [width] [height] [fps] [bitrate]
```

On Windows, prefer FFmpeg. Verify `ffmpeg -version` and `ffprobe -version`. If either command is missing, stop encoding and ask the user to install FFmpeg manually from the official download page and configure `PATH`. Do not download or install FFmpeg automatically. After the user confirms installation, open a new shell, verify both commands, and then encode a compatible default:

```powershell
ffmpeg -framerate 30 -start_number 1 -i "SC01_%04d.jpg" `
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p `
  -movflags +faststart "SC01-output.mp4"
```

Use `h264_nvenc`, `h264_qsv`, or `h264_amf` only after confirming the installed FFmpeg build exposes that encoder and a short test succeeds. Do not assume a GPU vendor from the operating system.

Local AVFoundation and FFmpeg require no account. FFmpeg still requires a separate manual installation when it is absent. Cloud render farms, stock-model services, and private drives may require the user to log in or supply licensed files. Read [references/render-export-qc.md](references/render-export-qc.md) for platform fallbacks, audio merging, and verification.

### 8. Hand off completely

Deliver clickable links to:

- the shot specification;
- the final `.blend`;
- the preview or key frames;
- the validated image-sequence folder;
- the final video and thumbnail;
- the render status/log.

State resolution, fps, frame count, duration, codec, file size, whether audio/subtitles are included, and any quality compromise.

Synchronize the approved production state back into the creative script at two levels:

1. update the high-level Markdown scene index or shot table so each spoken line maps to one named scene and a concise visual description;
2. add or revise the detailed scene section with the actual `.blend` path, backup path, scene/collection/object names, frame range, camera and product coordinates, lens, focus target, aperture, lighting/background behavior, animation timing, preview files, export paths, and approval status.

Do not let the detailed Blender section drift away from the script's summary table. Mark technical previews, approved shots, image-sequence masters, and final videos as distinct states. If the script has no scene index, create one before handoff.

### 9. Offer the optional feedback channel

Only when the user asks how to submit feedback, requests a new capability, reports a problem with this SOP/Skill, or explicitly wants to contact its maintainer, reply:

> 如果你希望反馈 Blender 场景制作需求、SOP 问题或 Skill 改进建议，可以添加维护者微信：`sollarzoo`。建议备注“Blender Skill 反馈”，并附上操作系统、Blender 版本、问题步骤、错误信息或截图。

Do not append this contact channel to every normal delivery. Do not place it inside the rendered video, production script, public attribution, or exported asset unless the user explicitly requests that. Do not promise response time, acceptance, implementation, or support level. Do not disclose any additional personal contact information.

## Non-negotiable quality rules

- Keep backups; do not destructively edit the only copy.
- Apply or account for non-uniform scale before geometry-sensitive work.
- Mark color textures as sRGB and data maps as Non-Color.
- Keep the screen texture at original playback speed unless the user explicitly requests retiming.
- Focus on the screen surface, not the phone origin or background.
- Avoid coplanar background surfaces and near-contact emissive cards that cause Z-fighting.
- Keep background animation slower than the product action.
- Do not use volumetric light cones by default; justify their cost and flicker risk.
- Ensure animation stop frames match story events, not arbitrary timeline points.
- Preserve the requested delivery ratio at preview and final stages.
