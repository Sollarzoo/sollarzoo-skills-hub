# Troubleshooting

## Background flickers while moving

Likely causes:

- coplanar surfaces causing Z-fighting;
- emissive/light-card geometry nearly touching the wall;
- viewport temporal sampling plus volumetrics;
- animated Noise changing too quickly;
- shadow-map instability or insufficient samples.

Fix in order:

1. inspect overlapping background objects and visibility;
2. keep one physical wall;
3. move or remove near-contact emissive cards;
4. remove unnecessary volume cones;
5. slow Shader animation and use smooth interpolation;
6. raise samples only after geometry is stable;
7. test a continuous 2–3 second segment.

## Screen looks gray

- Increase screen emission rather than front-light energy.
- Reduce screen/glass roughness.
- Use a broad, low-energy reflection source at an angle.
- Keep direct front fill weak enough that it does not wash out the UI.
- Confirm color management and image color space.

## Screen has top/bottom gaps

- Inspect UV bounds and video aspect ratio.
- Decide crop versus stretch explicitly.
- Scale/crop the video texture to fill the visible display.
- Check the screen mask and rounded-corner geometry.

## Screen or text is blurry

- Set final output resolution before judging.
- Focus DOF on a helper located on the screen plane.
- Use a less extreme aperture such as f/4–f/8.
- Check texture resolution and viewport/render sampling.
- Ensure motion blur is not smearing UI.

## Video looks accelerated

- Compare scene fps, source fps, image-user frame duration, and timeline length.
- Keep one source frame per intended timeline frame.
- Do not shorten the scene without an approved editorial cut.
- Validate duration with `frame_count / fps`.

## Camera pull-back has no depth

If the product and background appear glued together:

- keep the background fixed;
- let the product carry most of the depth change;
- use subtle camera movement for reframing;
- add foreground/background separation through lighting and DOF;
- avoid equal camera/product motion that cancels relative parallax.

## Background is black or invisible

- Confirm the wall is visible to viewport/render.
- Check normals and material output.
- Separate product-only and background-only lights where possible.
- Add low-level world/background fill or restrained material emission.
- Verify that a light is aimed at the wall rather than parallel to it.

## Lighting is chaotic or too expensive

- Isolate lights one at a time.
- Keep 5–8 documented roles.
- Remove duplicates and lights with no visible effect.
- Prefer large area lights for product reflections.
- Avoid volumes and excessive shadow-casting lights.

## Render takes too long

1. Decide whether the output is a review preview or hero final.
2. Use rendered viewport or Eevee for review.
3. export images first;
4. remove volumes, unused lights, hidden geometry, and expensive modifiers;
5. lower samples before lowering resolution or fps;
6. preserve requested duration and playback speed;
7. use VideoToolbox/AVFoundation or hardware FFmpeg for encoding.

## Image sequence stops

- Keep completed frames.
- Read `render_status.json`.
- Fix the error and resume from the first missing frame when the method supports it.
- Never delete a valid partial sequence until the replacement is confirmed.
