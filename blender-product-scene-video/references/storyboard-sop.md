# Image2 storyboard SOP

## Contents

1. Confirm prerequisites
2. Prepare reference inputs
3. Design storyboard coverage
4. Generate with Image2
5. Assemble the storyboard grid
6. Review and revise
7. Record approval and hand off to Blender
8. Return to storyboard when direction changes

## 1. Confirm prerequisites

Do not generate a production storyboard until the creative script is confirmed. The script must identify:

- the spoken line or message for each scene;
- the product feature or concept being shown;
- the opening and ending intent;
- the delivery ratio and approximate duration;
- visual restrictions and product-evidence boundaries.

Storyboard generation may expose a script problem. If it does, revise and reconfirm the script before continuing.

## 2. Prepare reference inputs

Use the strongest available evidence:

- clean product photographs or approved renders;
- real UI screenshots or frames extracted from the recording;
- brand colors, typography, and logo assets when relevant;
- one to three visual references for composition, lighting, or atmosphere;
- the preceding scene's approved final frame when continuity matters.

Crop and label references before generation. Distinguish identity references, composition references, and style references. Do not let a style reference replace the real product or UI.

## 3. Design storyboard coverage

For each scene, define a compact storyboard set:

1. opening frame;
2. hero or main-action frame;
3. ending frame or transition handoff.

Add another frame only when a distinct concept or transition cannot be understood from those three. Prefer one considered direction first. Generate up to three comparable alternatives only when a meaningful creative choice remains.

Annotate each frame with:

- scene id and spoken line;
- product position, scale, and angle;
- camera framing and implied movement;
- background or conceptual elements;
- lighting and reflection intent;
- what must remain readable;
- continuity from the previous scene;
- whether the image is product evidence or editorial concept.

## 4. Generate with Image2

Use an Image2-capable image model with the supplied product and UI references. Keep the prompt grounded in the confirmed script.

Preserve:

- device identity, proportions, camera layout, and materials;
- real UI layout and the specific content required by the scene;
- delivery aspect ratio and safe margins;
- continuity across frames.

Avoid:

- invented buttons, screens, notifications, or product behavior;
- changing phone identity between frames;
- decorative concepts that obscure the product priority;
- generating many unrelated options without a decision question.

Use static frames for storyboard approval. Image-to-video generation may be used later as a motion reference, but it does not replace the approved static composition set or the final Blender implementation.

## 5. Assemble the storyboard grid

The required review artifact is one storyboard contact-sheet image that shows all shots together. Do not ask the user to review only a folder of separate images.

Use these layout rules:

- order panels chronologically from left to right, then top to bottom;
- use a `2×2`, `3×2`, or another compact grid appropriate to the shot count;
- keep every panel at the same aspect ratio as the intended delivery frame;
- use visible, even gutters so adjacent frames do not merge;
- label each panel with scene and shot ids such as `SC01-01`;
- keep numbering, labels, and optional timing outside the important product area;
- use one image large enough that the phone pose, screen priority, lighting, and background remain judgeable;
- keep individual source frames as working files, but treat the grid image as the approval source of truth.

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

## 6. Review and revise

Present the storyboard grid image before Blender work. Ask the user to assess:

- Is the phone centered, scaled, and angled correctly?
- Does the chosen frame make the intended product feature obvious?
- Are story or concept elements helping rather than competing?
- Are reflections, lighting, and background appropriate?
- Does the ending composition connect to the next scene?

Revise the affected panels, rebuild the grid image, and request approval again when feedback changes composition, product pose, visual metaphor, environment, or overall lighting direction.

## 7. Record approval and hand off to Blender

Copy `assets/storyboard-template.md` and record:

- storyboard version, grid-image path, and generated panel paths;
- source script version;
- selected direction and rejected alternatives;
- user feedback and explicit approval status;
- approved composition, pose, lighting, background, and continuity notes;
- open technical questions for Blender.

Only a reviewed grid image plus `approved_for_blender` authorizes stage 3. Translate the approved panels into Blender camera, model, material, light, and animation specifications. Blender may solve geometry and timing, but it must not silently redesign the shot.

## 8. Return to storyboard when direction changes

Return to stage 2 if feedback changes any of these:

- core composition or camera angle;
- product pose, scale, or movement owner;
- setting, background concept, or visual metaphor;
- major lighting direction or reflection language;
- opening or ending state;
- scene-to-scene continuity.

Stay in Blender when the change is technical and preserves the approved image, such as fixing UVs, reducing flicker, correcting focus, tuning render samples, or making a small measured alignment correction.

Do not delete old Blender variants automatically. Stop producing new ones, label their status, and ask before cleanup.
