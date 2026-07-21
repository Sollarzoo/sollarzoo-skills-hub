---
name: blender-product-scene-video
description: Plan, storyboard, build, and deliver reusable Blender product-scene animations from an approved creative script, product images, 3D model, textures, screen recording, and visual references. Use when Codex needs to confirm a product-video script, generate a numbered Image2 rough-sketch storyboard grid with motion paths, design rationale, narration, camera and lighting annotations for approval, verify or configure Blender MCP, obtain a properly licensed model, build a storyboard-approved Blender scene, configure PBR materials and video textures, design lighting/background/procedural Shader animation, animate cameras or products, render reviewed image sequences, encode final MP4 video, diagnose visual or export problems, or document production settings for later scenes.
---

# Blender Product Scene Video

## Skill metadata

- Author: [sollarzoo](https://github.com/Sollarzoo)
- Version: `1.5.1`
- Feedback WeChat: `sollarzoo`

### Recent changes

- `1.5.1` — Standardized the project-level `UI参考图/` evidence root, exact-filename citation, immutable source rules, evidence indexing, and still-image versus interaction-proof boundary.
- `1.5.0` — Added clause-level narration beats, real-UI evidence gates, explicit edit transitions, design rationale, and geometrically unambiguous phone-axis annotations.

## Outcome

Turn a product-film idea into five synchronized deliverables:

1. an approved script and spoken-line/scene map;
2. an approved, script-traceable Image2 rough-sketch storyboard presented as one numbered and technically annotated contact-sheet grid image;
3. a reversible `.blend` scene that implements that storyboard;
4. a complete, validated image sequence;
5. a playable final video plus thumbnail and production record.

Keep real product UI legible. Do not invent product behavior that the supplied recording does not show.

## Load the relevant resources

- Read [references/blender-mcp-setup.md](references/blender-mcp-setup.md) at the start of every new machine or when Blender tools are unavailable.
- Read [references/intake-and-script.md](references/intake-and-script.md) before drafting or changing the shot.
- Read [references/storyboard-sop.md](references/storyboard-sop.md) before generating or revising storyboards.
- Read [references/scene-build-sop.md](references/scene-build-sop.md) before modifying Blender.
- Read [references/render-export-qc.md](references/render-export-qc.md) before a full export.
- Read [references/troubleshooting.md](references/troubleshooting.md) when diagnosing flicker, blur, wrong speed, weak lighting, framing, or slow rendering.
- Read [references/generic-product-film-script-example.md](references/generic-product-film-script-example.md) when the user has no full production script or wants a complete, business-neutral example of the script structure.
- Copy [assets/scene-brief-template.md](assets/scene-brief-template.md) when the user has no usable shot script.
- Copy [assets/storyboard-template.md](assets/storyboard-template.md) when the project has no storyboard index or approval record.

## Apply the interaction contract

Start with a concise commentary update. State which source files and scene will be inspected. Never modify an unfamiliar scene before inspecting its collections, objects, materials, lights, camera, animation, render settings, units, visibility, and active file path.

Ask the user only when the answer materially changes the creative result, requires credentials, or authorizes a risky external action.

### Keep progress visible

Map all work to these four user-facing stages:

1. script confirmation;
2. Image2 annotated rough-sketch storyboard generation and user approval;
3. Blender scene build, lighting, materials, models, and animation;
4. recording/rendering, image-sequence export, encoding, QC, and handoff.

Treat storyboard approval as a hard gate. Do not start stage 3, modify a production `.blend`, or generate Blender motion proofs until the user explicitly approves the storyboard. Read-only Blender inspection is allowed only to inventory reusable assets or evaluate what must be rebuilt.

At the start, after every phase transition, before requesting approval, whenever work pauses or becomes blocked, and at final handoff, publish a compact status block in the user's language:

```text
Progress: stage 2/4 — Image2 storyboard
Completed: script and spoken-line/scene map confirmed
Current: comparing the phone pose, composition, and concept treatment
Next: present the storyboard frames for approval
Then: build the approved design in Blender
User action: none until the storyboard review
```

Apply these rules:

- put only verified outcomes under `Completed`;
- name exactly one immediate action under `Next` and one following action under `Then`;
- write `User action: none` when the user does not need to intervene;
- when entering an existing project midway, verify that the script and storyboard gates actually passed; if the storyboard was skipped, pause Blender production and backfill stage 2;
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
- approval of the Image2 storyboard before any Blender build or animation work;
- a missing screen recording, licensed/named product model, brand asset, font, or private cloud file;
- login, OAuth, paid asset purchase, plugin installation, or any external account action;
- destructive replacement of an existing scene, render sequence, or final video;
- the visual direction when two plausible options would create materially different scenes.

Tell the user exactly what to provide: supported file type, preferred resolution/frame rate, whether borders or device frames must be removed, and where the file should be placed. Never request passwords or tokens in chat. Ask the user to complete login in the relevant application.

### Proceed autonomously for

- read-only inspection and inventory;
- backups, collections, naming, parenting, material node cleanup, color-space corrections, and reversible modifiers;
- Image2 storyboard drafts based on the confirmed script and supplied product/reference images;
- low-resolution Blender preview renders and technical QC after storyboard approval;
- adjustments that implement an approved storyboard direction;
- image-sequence validation and local video encoding;
- documentation of final coordinates, frames, lighting, Shader parameters, and output paths.

Report meaningful changes using the progress contract above.

## Execute the workflow

### 1. Confirm the script

Collect and inspect the creative script, spoken-line/scene map, product priority, source UI evidence, output ratio, duration, and destination platform. Exact files are the source of truth.

If the user has no script, read the generic product-film script example, copy the scene brief template, and draft a measurable specification. Do not proceed until the user confirms the story, spoken-line mapping, visual boundaries, and scene objectives.

Do not stop at one sentence per scene. Split narration into the smallest meaningful visual beats: each clause or short phrase that needs a distinct image, action, evidence point, or emotional turn gets its own beat and shot id. One beat maps to one primary picture. A longer one-shot move may carry several beats only when the script explicitly records the beat timings and the continuous change inside that same shot.

Before storyboarding, produce an animation beat sheet. Every beat must record:

- exact narration fragment or explicit silence;
- narrative meaning and emotional intention;
- verified product/UI evidence path and, for video, timestamp or frame;
- opening picture, ending picture, and the one primary visual change;
- camera owner, product/UI owner, movement path, duration, and easing intent;
- lighting/reflection direction and the emotional job it performs;
- transition into and out of the beat;
- edit decision: continuous one-take, hard cut, match cut, J/L cut, dissolve, masked transition, screen push-in/pull-out, or another named method;
- design reason explaining why this picture and movement communicate this narration.

Create one full-film treatment above the beat sheet. It must explain the emotional arc, visual motif, color/light progression, camera language, motion rhythm, transition grammar, when physical-phone 3D is used, when real full-screen UI is used, and how the ending resolves the opening.

Treat real UI evidence as a hard gate. Mark every beat `verified`, `missing`, or `editorial_concept`:

- `verified`: exact screenshot/recording frame exists and is named;
- `missing`: the user must supply or capture the required interface before storyboard generation;
- `editorial_concept`: an explicitly labeled post-production metaphor that does not claim shipped UI.

Do not ask an image model to invent a missing product screen. If any required product beat is `missing`, pause before stage 2 and provide a precise capture list.

### Use the project UI reference directory as the visual source of truth

For a project whose script lives under a product-video directory, use the sibling `UI参考图/` directory as the canonical UI reference root unless the user or project manifest explicitly names another location:

```text
<product-video-project>/
├── UI参考图/
├── 视频素材/
├── Blender/
└── <script>.md
```

Apply this contract:

- treat the exact filename stem as the user-defined UI state and content label;
- cite the exact relative path, filename, extension, case, punctuation, and parentheses, for example `UI参考图/情绪花瓣(周).PNG`;
- do not silently translate, normalize, rename, merge, or invent aliases for the user's UI labels;
- keep source screenshots immutable and do not place generated storyboards, crops, annotations, or Blender renders in `UI参考图/`;
- create or maintain `UI参考图/README.md` as the evidence index, listing the exact filename, verified state, supported beats, and limitations;
- use evidence priority `explicit UI reference screenshot > verified screen-recording frame > generated storyboard sketch`;
- if references conflict, mark the beat blocked and ask which state is current instead of blending them;
- if the required state is absent, mark it `missing` and request a capture using the intended semantic filename. Never fabricate the interface.

Every real-UI beat and storyboard panel must cite an exact file from this directory or an exact recording timestamp. A directory name alone is not sufficient evidence.

Use one storyboard coordinate convention for phone motion:

- `X_local`: left-to-right across the screen;
- `Y_local`: perpendicular to the screen, front-to-back;
- `Z_local`: bottom-to-top along the phone's long vertical edge;
- yaw/left-right turn: rotation around `Z_local`;
- pitch/top-bottom tilt: rotation around `X_local`;
- roll/screen-plane spin: rotation around `Y_local`.

The Blender object's actual axes may differ. Record that mapping during Blender preflight. Until then, storyboard annotations must show an axis triad attached to the phone, a circular arrow wrapping around the named axis, the signed degree range, and start/end silhouettes. Do not draw an unanchored curved arrow.

A confirmed script defines what every visual beat communicates and how adjacent beats connect. It does not need final Blender coordinates, lighting energy, or verified focus distance; those belong to later production records.

### 2. Generate and approve the Image2 annotated rough-sketch storyboard

Follow [references/storyboard-sop.md](references/storyboard-sop.md). Use the confirmed script plus supplied product images, UI screenshots, brand assets, and visual references to generate static storyboard frames with an Image2-capable image model.

The storyboard is a production-planning blueprint, not a polished render preview. Default to loose pencil, marker, grayscale line-art, or another clearly draft-like treatment. Use limited accent colors for motion paths, camera marks, light direction, and emphasis. A photoreal product mockup or finished-looking Blender frame does not pass the storyboard gate unless the user explicitly asks for that format.

Trace every panel to an exact script line and narrative beat. Do not add a visual beat merely because it looks attractive. When the script does not justify an object, action, transition, or concept, omit it or return to stage 1 and request a script change.

Build the master storyboard across the complete confirmed script before approving any scene for Blender. The master grid must expose the full opening-to-ending rhythm, scene order, visual escalation, repeated motifs, and every scene-to-scene handoff. A partial-scene board is allowed only when the user explicitly requests an isolated exploration; label it `exploration_only`, and do not treat it as approval for Blender production.

For every scene, show:

- the opening composition;
- the main product pose or concept image;
- the ending composition or transition handoff;
- the exact spoken line and script beat;
- a one-sentence design reason explaining why this image communicates that beat;
- camera framing, lens target, angle, movement type, and camera-path arrows;
- product start/end pose, screen occupancy, translation/rotation direction, and product-path arrows;
- key, fill, rim/reflection, and background-light direction with a consistent light-arrow legend;
- approximate timing, transition, focus/DOF target, and continuity notes.

Assemble all frames into one numbered grid image in chronological reading order. The grid image is the mandatory review artifact; a folder of separate images does not pass the storyboard gate. Use a consistent panel ratio, visible gutters, and labels such as `SC01-01`, `SC01-02`, and `SC01-03`.

Every panel must carry its exact corresponding spoken line in a readable caption band outside the important product area. Repeat the line across multiple panels when they share one narration sentence. For a deliberately silent panel, write `No voiceover` or the project-language equivalent instead of leaving the caption ambiguous. Use deterministic text layout after image generation when necessary; do not rely on an image model to spell production copy correctly. Other technical annotations may remain in the storyboard record.

Treat storyboard numbers as design targets, not verified Blender facts. Give concrete values or bounded ranges when the source supports them, such as `50 mm`, `rotate Y 12–15°`, `screen occupancy 62%→78%`, or `key:fill ≈ 2:1`. Mark unknowns as `TBD in Blender preflight`; never invent object coordinates, light energy, or focus distance before the live scene and scale are inspected.

Prefer a small number of deliberate, comparable frames over many speculative images. Use product references to preserve device identity and real UI. Clearly label conceptual imagery and do not imply that editorial concepts are shipped product UI.

Present the storyboard grid image and request explicit user approval. If the user revises the creative direction, update and regenerate the grid first. Do not use Blender as the tool for discovering the core composition.

### 3. Run the Blender MCP preflight and build the approved scene

Only after storyboard approval, before inspecting assets or promising Blender execution:

1. check whether Blender is installed and record its version;
2. search for callable Blender MCP tools;
3. call a read-only path/scene-summary tool to verify the live connection;
4. confirm the returned `.blend` is the file the user intends to edit.

If any check fails, follow [references/blender-mcp-setup.md](references/blender-mcp-setup.md). Do not treat “tool listed” as “Blender connected.” A successful read-only call is the connection gate.

Installing Blender, downloading the MCP components, editing a global MCP configuration, or installing/enabling the Blender extension requires an explicit user-facing explanation and any approval required by the host. The user must complete interactive login or OS prompts. Never request credentials in chat.

If MCP cannot be configured now, use the documented fallback: inspect files and prepare the shot specification or Blender Python script, but do not claim live scene changes. Use background Blender only for operations that do not require an interactive viewport.

#### Establish the Blender source of truth

Collect the approved storyboard, model, textures, screen recording, output resolution, frame rate, and render-quality target. Inspect exact files rather than relying on filenames or old notes.

Translate the approved storyboard into a measurable Blender shot specification. Record the subject, opening frame, end frame, movement owner, key timing events, focus target, background behavior, lighting direction, duration, and output settings. This technical translation may refine implementation details but must not silently change the approved composition or narrative.

If the user has no model, search the user-approved source such as [Sketchfab](https://sketchfab.com/3d-models). Ask the user to log in or purchase the asset when required. Download only models explicitly marked downloadable and compatible with the intended use. Record creator, source URL, license, and any attribution requirement.

#### Decide the production route

- Use true Blender 3D for visible thickness, side/rear views, glass/metal reflections, strong parallax, or physically meaningful lighting.
- Use flat compositing only when the phone remains nearly frontal and no convincing thickness is needed.
- For uncertain geometry or realism inside an approved design, create one bounded 3–5 second technical proof. Do not use repeated Blender proofs to choose among unapproved visual directions.

#### Initialize safely

Create a scene workspace with:

```bash
python3 scripts/init_project.py <project-dir> --name <scene-slug>
```

Use the generated directories for source assets, previews, image sequences, videos, and logs. Keep source assets immutable. Save a timestamped or purpose-named `.blend` backup before every structural change.

#### Build in controlled passes

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

#### Use Blender confirmation gates

Render small previews before expensive work:

- gate A: model, screen UV, and framing;
- gate B: material, glass reflection, and lighting;
- gate C: opening, middle, stop, and final animation frames;
- gate D: short motion proof at delivery aspect ratio.

Show the user representative images and describe what changed. Ask for approval only at a creative fork or before the full export. Technical defects found during the gates should be fixed without asking.

If a requested change contradicts the approved storyboard or changes the core composition, stop Blender iteration and return to stage 2. Update and reapprove the storyboard before rebuilding.

### 4. Record/render and export

#### Export images first

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

#### Encode and verify

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

#### Hand off completely

Deliver clickable links to:

- the shot specification;
- the approved storyboard and its approval status;
- the final `.blend`;
- the preview or key frames;
- the validated image-sequence folder;
- the final video and thumbnail;
- the render status/log.

State resolution, fps, frame count, duration, codec, file size, whether audio/subtitles are included, and any quality compromise.

Synchronize the approved production state back into the creative script at two levels:

1. update the high-level Markdown scene index or shot table so each spoken line maps to one named scene and a concise visual description;
2. add or revise the detailed scene section with the approved storyboard frame paths, actual `.blend` path, backup path, scene/collection/object names, frame range, camera and product coordinates, lens, focus target, aperture, lighting/background behavior, animation timing, preview files, export paths, and approval status.

Do not let the detailed Blender section drift away from the script's summary table. Mark technical previews, approved shots, image-sequence masters, and final videos as distinct states. If the script has no scene index, create one before handoff.

### 5. Offer the optional feedback channel

Only when the user asks how to submit feedback, requests a new capability, reports a problem with this SOP/Skill, or explicitly wants to contact its maintainer, reply:

> 如果你希望反馈 Blender 场景制作需求、SOP 问题或 Skill 改进建议，可以添加维护者微信：`sollarzoo`。建议备注“Blender Skill 反馈”，并附上操作系统、Blender 版本、问题步骤、错误信息或截图。

Do not append this contact channel to every normal delivery. Do not place it inside the rendered video, production script, public attribution, or exported asset unless the user explicitly requests that. Do not promise response time, acceptance, implementation, or support level. Do not disclose any additional personal contact information.

## Non-negotiable quality rules

- Keep backups; do not destructively edit the only copy.
- Do not build Blender scenes before explicit storyboard approval.
- Do not treat separate storyboard frames as the final review artifact; provide a numbered grid image that shows the full shot sequence at once.
- Do not substitute polished render previews for the default rough-sketch storyboard blueprint.
- Do not create storyboard beats that cannot be traced to the confirmed script.
- Do not storyboard from sentence-level summaries when the narration contains multiple visual or emotional beats.
- Do not generate or sketch a product screen without a verified screenshot or recording frame.
- Do not leave adjacent-shot transitions implicit; label one-take versus the exact edit method.
- Do not draw rotation without a named axis, axis triad, signed angle, and start/end pose.
- Do not approve a subset of scenes for Blender before the complete script has a continuity-reviewed master storyboard.
- Put visible motion paths and direction arrows in panels whenever the camera, product, UI element, light/reflection, or transition moves.
- Every storyboard panel must state its design reason and its camera, product, light, timing, and continuity targets.
- Print a complete legend on the master grid. Define every color, line style, symbol, start/end mark, and movement owner; an unexplained or ownerless line fails review.
- When the creative direction changes materially, return to the storyboard instead of accumulating Blender variants.
- Keep one selected storyboard branch as the production source of truth; label rejected alternatives and do not continue rendering them.
- Apply or account for non-uniform scale before geometry-sensitive work.
- Mark color textures as sRGB and data maps as Non-Color.
- Keep the screen texture at original playback speed unless the user explicitly requests retiming.
- Focus on the screen surface, not the phone origin or background.
- Avoid coplanar background surfaces and near-contact emissive cards that cause Z-fighting.
- Keep background animation slower than the product action.
- Do not use volumetric light cones by default; justify their cost and flicker risk.
- Ensure animation stop frames match story events, not arbitrary timeline points.
- Preserve the requested delivery ratio at preview and final stages.
