# Image2 storyboard SOP

## Contents

1. Confirm prerequisites
2. Prepare reference inputs
3. Design storyboard coverage
4. Generate the rough-sketch frames with Image2
5. Add production annotations and motion paths
6. Assemble the storyboard grid
7. Review and revise
8. Record approval and hand off to Blender
9. Return to storyboard when direction changes

## 1. Confirm prerequisites

Do not generate a production storyboard until the creative script is confirmed. The script must identify:

- the exact narration fragment for each clause-level visual beat;
- the product feature or concept being shown;
- the verified screenshot/recording evidence for every real product beat;
- the emotional intention and design reason for every beat;
- movement owner, opening/ending state, timing, easing, and light intent;
- whether every beat boundary is one-take or a named edit/transition method;
- the opening and ending intent;
- the delivery ratio and approximate duration;
- visual restrictions and product-evidence boundaries.

Storyboard generation may expose a script problem. If it does, revise and reconfirm the script before continuing.

Create a traceability map before drawing:

| Panel id | Exact script line | Narrative beat | Required product evidence |
|---|---|---|---|
| SC01-01 | verbatim line | one beat only | source screenshot/recording/model |

Every panel must have one row. If a planned panel has no defensible script beat, remove it. If a script beat has no panel, add one or document why it is intentionally carried by an adjacent panel.

Default mapping is one narration beat to one storyboard panel. Do not repeat the whole sentence under several generic opening/middle/ending panels. If one continuous shot carries multiple narration beats, draw separate beat-state panels and label them as one-take key states on the same shot timeline.

Storyboard the complete confirmed script as one master sequence before approving Blender work. The master review must cover:

- every scene and spoken line, including deliberate silence;
- opening and final brand/interaction frames;
- each scene-to-scene entry and exit composition;
- visual rhythm across the whole duration;
- repeated product poses, UI motifs, color progression, and transitions;
- whether later scenes resolve promises established earlier.

Partial boards are useful only for explicitly requested exploration. Mark them `exploration_only`; they cannot set `approved_for_blender: true`.

## 2. Prepare reference inputs

Use the strongest available evidence:

- clean product photographs or approved renders;
- real UI screenshots or frames extracted from the recording;
- brand colors, typography, and logo assets when relevant;
- one to three visual references for composition, lighting, or atmosphere;
- the preceding scene's approved final frame when continuity matters.

Crop and label references before generation. Distinguish identity references, composition references, and style references. Do not let a style reference replace the real product or UI.

When the project contains `UI参考图/`:

- use it as the canonical UI screenshot root;
- inspect `UI参考图/README.md` and the source image;
- cite the exact filename in every real-UI panel, such as `UI参考图/每周来信(展开).PNG`;
- retain the filename stem as the UI-state label;
- never substitute a generated approximation for the cited screenshot;
- keep crops and annotated copies in the storyboard workspace, not inside `UI参考图/`.

A still screenshot verifies composition and visible content only. Do not use it as evidence of a tap, swipe, save, transition, or loading sequence unless a recording or multiple verified states support that action.

## 3. Design storyboard coverage

For each scene, define a compact storyboard set:

1. opening frame;
2. hero or main-action frame;
3. ending frame or transition handoff.

Add another frame only when a distinct concept or transition cannot be understood from those three. Prefer one considered direction first. Generate up to three comparable alternatives only when a meaningful creative choice remains.

Annotate each frame with:

- scene id and spoken line;
- the exact script beat represented by this frame;
- a one-sentence design reason;
- product position, scale, and angle;
- camera framing and implied movement;
- background or conceptual elements;
- lighting and reflection intent;
- what must remain readable;
- continuity from the previous scene;
- whether the image is product evidence or editorial concept.

## 4. Generate the rough-sketch frames with Image2

Use an Image2-capable image model with the supplied product and UI references. Keep the prompt grounded in the confirmed script.

Default visual language:

- loose storyboard pencil or marker linework;
- grayscale or warm paper background;
- simplified product geometry that preserves the phone silhouette and important UI hierarchy;
- one to three accent colors reserved for paths, light arrows, focus marks, and critical UI;
- clear negative space for technical notes;
- draft-like, editable thinking rather than polished advertising imagery.

Do not generate a photoreal contact sheet by default. Product screenshots may be inserted as small evidence callouts when exact UI readability matters, but the surrounding shot should remain a storyboard drawing.

Preserve:

- device identity, proportions, camera layout, and materials;
- real UI layout and the specific content required by the scene;
- delivery aspect ratio and safe margins;
- continuity across frames.

Avoid:

- invented buttons, screens, notifications, or product behavior;
- any product UI panel whose evidence status is `missing`;
- changing phone identity between frames;
- decorative concepts that obscure the product priority;
- generating many unrelated options without a decision question.

Use static frames for storyboard approval. Image-to-video generation may be used later as a motion reference, but it does not replace the approved static composition set or the final Blender implementation.

## 5. Add production annotations and motion paths

Each panel must be understandable without opening a separate Markdown file. Draw directly on or around the sketch:

- solid arrow: product/object path;
- double-line or camera-icon arrow: camera path;
- curved arrow: rotation, with axis and degree target;
- dashed arrow: transition or UI-element path;
- ray/cone arrow: key, fill, rim/reflection, or background-light direction;
- focus box or target mark: focus/DOF target;
- `START` and `END` marks when one panel describes a move.

Include a small technical block for every panel:

| Field | Required content |
|---|---|
| Shot | scene/shot id, duration or timecode |
| Narration | exact script line, or explicit no-voiceover label |
| Why | one-sentence design reason tied to the script beat |
| Camera | shot size, angle, lens target, locked/dolly/pan/tilt/zoom, path |
| Product | start/end position, screen occupancy, translation and rotation target |
| Focus | UI/physical focus target and approximate aperture intent |
| Lighting | key/fill/rim/background direction, color intent, relative ratio |
| Timing | key moments and easing intent |
| Continuity | entry from the previous panel and handoff to the next |

For phone rotation, draw a phone-local axis triad on the subject. The circular arrow must visibly wrap around `X_local`, `Y_local`, or `Z_local`; add signed start/end angles and a small start/end silhouette. State whether the camera is locked. Do not use a free-floating loop that could mean orbit, roll, yaw, or camera movement.

At every panel boundary, write one of:

- `ONE TAKE` plus the continuous movement that bridges the two states;
- `HARD CUT`;
- `MATCH CUT` plus the matched shape/position;
- `J CUT` or `L CUT` plus the audio overlap;
- `DISSOLVE` plus duration;
- `MASKED TRANSITION` plus masking object;
- `SCREEN PUSH-IN` / `SCREEN PULL-OUT`;
- another explicit edit method with duration.

Use concrete design targets where defensible: `50 mm`, `Y rotation 12–15°`, `screen occupancy 62%→78%`, `key 4300 K`, or `key:fill ≈ 2:1`. Use bounded ranges when exact values will be tuned later. Write `TBD in Blender preflight` for scale-dependent coordinates, light energy, focus distance, or other values that cannot be known before scene inspection.

Keep a consistent legend across the whole grid and print it once in the margin. The legend must define:

- black/gray sketch lines: static subject, UI, environment, and frame boundaries;
- blue solid arrows: product, card, or UI-element movement;
- blue double-line arrows plus a camera label/icon: camera movement;
- blue curved arrows: rotation, including axis and degree target;
- blue dashed arrows: transition, date progression, or editorial-layer movement;
- yellow rays/arrows: key-light direction or primary visual emphasis;
- cyan rays/arrows: rim light, screen-glass reflection, or background-light sweep;
- focus box/crosshair: focus or DOF target;
- camera-lock icon: camera remains fixed;
- `S` and `E`: start and end state.

If the project uses another palette, write the replacement mapping explicitly. Do not use arrows decoratively; every arrow must name its owner and direction. An unexplained or ownerless line fails the storyboard gate.

## 6. Assemble the storyboard grid

The required review artifact is one storyboard contact-sheet image that shows all shots together. Do not ask the user to review only a folder of separate images.

Use these layout rules:

- order panels chronologically from left to right, then top to bottom;
- use a `2×2`, `3×2`, or another compact grid appropriate to the shot count;
- keep every panel at the same aspect ratio as the intended delivery frame;
- use visible, even gutters so adjacent frames do not merge;
- label each panel with scene and shot ids such as `SC01-01`;
- keep the visual treatment visibly sketch-like and unfinished;
- place the exact corresponding spoken line under every panel in a readable caption band;
- repeat the spoken line when several panels share one narration sentence, and explicitly label deliberately silent panels;
- typeset production copy deterministically after generation when needed instead of trusting generated text;
- include the design reason and compact camera/product/light/timing parameter block for every panel;
- draw the required camera, product, rotation, light/reflection, focus, and transition paths;
- include a single grid-wide arrow and color legend;
- keep numbering, narration, labels, and optional timing outside the important product area;
- use one image large enough that the phone pose, screen priority, lighting, and background remain judgeable;
- keep individual source frames as working files, but treat the grid image as the approval source of truth.

For a long film, produce one zoomable, high-resolution master grid that contains every panel. Optional per-scene detail grids may accompany it, but they do not replace the all-scene master.

Recommended output:

```text
storyboards/SC01-v1/
├── panels/
│   ├── SC01-01-opening.png
│   ├── SC01-02-hero.png
│   └── SC01-03-ending.png
└── SC01-storyboard-grid-v1.png
```

If the grid contains multiple scenes, keep globally clear numbering and add scene-divider labels without breaking chronological order.

## 7. Review and revise

Present the storyboard grid image before Blender work. Ask the user to assess:

- Is the phone centered, scaled, and angled correctly?
- Does the chosen frame make the intended product feature obvious?
- Can every visual choice be traced back to the confirmed script?
- Does every panel show exactly one narration beat rather than an over-broad sentence?
- Does every panel explain why the design supports that line?
- Does each product panel cite real UI evidence?
- Is each boundary explicitly one-take or a named edit?
- Is every rotation axis geometrically unambiguous?
- Are all intended movements visible as labeled paths or arrows?
- Are camera, product, light, timing, focus, and continuity targets specific enough to build?
- Are story or concept elements helping rather than competing?
- Are reflections, lighting, and background appropriate?
- Does the ending composition connect to the next scene?
- Does the complete sequence remain continuous and cumulative from the opening through the final frame?

Revise the affected panels, rebuild the grid image, and request approval again when feedback changes composition, product pose, visual metaphor, environment, or overall lighting direction.

## 8. Record approval and hand off to Blender

Copy `assets/storyboard-template.md` and record:

- storyboard version, grid-image path, and generated panel paths;
- source script version;
- selected direction and rejected alternatives;
- user feedback and explicit approval status;
- approved composition, pose, lighting, background, and continuity notes;
- open technical questions for Blender.

Only a reviewed grid image plus `approved_for_blender` authorizes stage 3. Translate the approved panels into Blender camera, model, material, light, and animation specifications. Blender may solve geometry and timing, but it must not silently redesign the shot.

## 9. Return to storyboard when direction changes

Return to stage 2 if feedback changes any of these:

- core composition or camera angle;
- product pose, scale, or movement owner;
- setting, background concept, or visual metaphor;
- major lighting direction or reflection language;
- opening or ending state;
- scene-to-scene continuity.

Stay in Blender when the change is technical and preserves the approved image, such as fixing UVs, reducing flicker, correcting focus, tuning render samples, or making a small measured alignment correction.

Do not delete old Blender variants automatically. Stop producing new ones, label their status, and ask before cleanup.
