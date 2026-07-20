# Blender scene-build SOP

## Contents

1. Verify the storyboard gate
2. Inspect and back up
3. Initialize and organize
4. Load and normalize the model
5. Build materials and screen
6. Compose camera and focus
7. Design product lighting
8. Build background and Shader
9. Animate
10. Optimize and preview

## 1. Verify the storyboard gate

Before any production edit, open the storyboard record and verify:

- `approved_for_blender: true`;
- the approved storyboard-grid path and source panel paths exist;
- the source script version is recorded;
- product pose, camera composition, background, lighting/reflection, and continuity are annotated.

If the gate is absent or ambiguous, stop after read-only inventory and return to the Image2 storyboard stage. Do not use Blender variants to replace the missing creative decision.

## 2. Inspect and back up

Connect to the current Blender scene and inspect without modifying:

- `.blend` path, dirty state, Blender version, render engine, units;
- scene and collection hierarchy;
- object names, types, transforms, parents, visibility;
- mesh modifiers, shared datablocks, UV maps, material slots;
- image and movie textures, paths, color spaces;
- camera, lens, constraints, depth of field;
- lights, energy, size, color, targets, animation;
- frame range, fps, resolution, markers, actions and drivers.

Do not dump a large scene blindly. Start with counts and collections, then inspect relevant objects. Save a named backup such as `scene-before-lighting.blend` before structural changes.

## 3. Initialize and organize

Use collections:

```text
SC##_PRODUCT
SC##_LIGHTS_PRODUCT
SC##_BACKGROUND
SC##_LIGHTS_BACKGROUND
SC##_CAMERA
SC##_HELPERS
```

Use role-based names. Create a single product root such as `SC##_ProductRig`. Parent the device, screen focus, reflection cards, and product lights that must keep a constant relationship to the product. Keep the physical background and background lights outside that rig.

## 4. Load and normalize the model

1. Import the supplied format with the standard Blender operator.
2. Capture actual returned objects; do not assume names.
3. Check scene units and model bounding box.
4. Correct orientation and scale at the root where possible.
5. Apply scale before booleans, bevels, displacement, or other scale-sensitive operations.
6. Inspect normals and shading; use Auto Smooth/weighted normals only when appropriate for the Blender version.
7. Preserve adjustable bevel and subdivision modifiers until final approval.
8. Place the product at a meaningful world origin and create an empty rig for animation.

For named commercial hardware, use only a user-provided or licensed model.

## 5. Build materials and screen

### PBR rules

- Base Color/Albedo: sRGB.
- Roughness, Metallic, Normal, Height, masks: Non-Color.
- Normal maps: Image Texture → Normal Map → Principled BSDF Normal.
- Metal: metallic near 1 with finish controlled mainly by roughness.
- Glass: use Principled transmission/coat and real reflections; avoid making the screen gray with excessive roughness.
- Make a shared material single-user before changing it if the change must affect only one object.

### Screen rules

1. Identify the visible screen mesh and its UV orientation.
2. Fit the image/video to the screen bounds without top or bottom gaps.
3. Preserve aspect ratio by cropping intentionally, not by accidental stretch.
4. Use the movie texture’s real frame rate and duration.
5. Drive the screen with emission plus controlled Principled reflection:
   - emission preserves UI brightness;
   - low roughness/coat creates glass reflection;
   - a broad, weak reflection source creates readable highlights without washing out UI.
6. Test an edge frame and a center frame for UV alignment.

Keep direct front light modest. Use side/rim/reflection lights for form, plus only enough front fill to reveal glass and bezel.

## 6. Compose camera and focus

- Set final output ratio before judging composition.
- Use a camera target empty instead of hand-keyframing rotation when the subject must remain centered.
- Keep a separate `SC##_ScreenFocus` object on the screen plane and use it as the DOF focus target.
- Prefer a moderate aperture such as f/4–f/8 for readable UI; lower values require a deliberate shallow-focus look.
- Keep the camera close to frontal for UI legibility. Introduce angle only when the model’s thickness or material needs to read.

For a hybrid pull-back:

1. animate the product rig for the majority of depth change;
2. animate the camera more subtly for reframing;
3. parent product lights and screen focus to the product rig;
4. keep the background unparented;
5. set exact stop keyframes for the product, camera, and target;
6. hold those values through the final frame.

Use timeline markers for story events such as typing start, send complete, full-product arrival, feature transition, and end.

## 7. Design product lighting

Start with 5–8 lights:

| Role | Purpose |
|---|---|
| Key | Main form and material direction |
| Soft front fill | Reveal bezel/glass without flattening |
| Rim | Separate edge from background |
| Upper side | Create controlled glass reflection |
| Lower side | Recover dark lower frame |
| Background key/fill | Shape only the wall/background |

Keep a coherent direction, for example upper-left to lower-right. Use large area lights for soft reflections and spotlights only for controlled accents. Lower saturation before adding more colors.

Evaluate each light by toggling it alone and then in the full rig. Delete or disable lights with no visible function. Do not keep dozens of legacy lights merely because they exist.

Avoid volumetric cones unless the story requires visible atmosphere. They increase render cost and can flicker in viewport export.

## 8. Build background and Shader

Prefer one physical background wall or cyclorama. Disable overlapping coplanar surfaces to prevent Z-fighting.

For a flowing abstract background:

1. use Generated/Object coordinates;
2. rotate coordinates diagonally;
3. combine Wave/Voronoi/Noise textures at different scales;
4. use ColorRamp to mix restrained sky blue, moss/forest green, warm white, or the approved palette;
5. add a very low-strength emission only if needed;
6. animate 4D Noise `W`, Mapping location, or texture phase slowly;
7. keep interpolation smooth and animation slower than product movement.

Do not place emissive cards nearly coplanar with the wall. If a light should appear on a wall, use a real light or incorporate the glow into one background material.

## 9. Animate

1. Convert script seconds to frames using the exact fps.
2. Create story-event markers first.
3. Key the opening, event/stop, and final hold before adding intermediate easing.
4. Use Bezier/auto-clamped-style easing where supported; inspect for overshoot.
5. Keep screen playback at original speed unless explicitly retimed.
6. Animate background Shader separately from transforms.
7. Check evaluated world positions, not only local properties, after parenting.

Do not accelerate a one-minute source recording to fit a shorter arbitrary timeline. Change the scene duration or edit the story with user approval.

## 10. Optimize and preview

- Use Eevee for fast product-film iterations unless Cycles-specific realism is required.
- Disable unused lights, hidden geometry, duplicate backgrounds, volumes, and expensive modifiers.
- Preview at 25–50% resolution.
- Check opening, middle, stop, and final frames.
- Render a short continuous segment to expose flicker that still images cannot show.
- Save after validation and record exact settings in the creative script.
