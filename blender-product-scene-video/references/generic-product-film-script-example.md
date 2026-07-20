# Generic Product Film Script Example

## Contents

1. How to use this example
2. Production positioning
3. Evidence and constraints
4. Master timeline
5. Scene and spoken-line index
6. Image2 storyboard plan and approval
7. Detailed Blender scene specification
8. Asset checklist
9. Preview and export gates
10. Production status and handoff

## 1. How to use this example

Use this document only as a structural reference when no production script exists.

- Replace every bracketed placeholder with information from the real brief, assets, and live product.
- Delete sections that do not apply.
- Measure coordinates, frames, durations, and render settings from the actual Blender scene.
- Do not copy example claims into a real script without product evidence.
- Keep the master timeline, scene index, and detailed Blender sections synchronized.
- Confirm the script first, then approve one numbered Image2 storyboard grid before Blender production.
- Mark drafts, technical previews, approved shots, image-sequence masters, and final videos as different states.

The example intentionally contains no real company, product, feature, customer, campaign, private path, or business metric.

## 2. Production positioning

### Working title

`[Short product-film title]`

### Audience takeaway

After watching, the audience should be able to repeat one sentence:

> `[The single verified product result or value the film demonstrates.]`

### Delivery format

- Master duration: `[for example, 30–60 seconds]`
- Aspect ratio: `[9:16 / 16:9 / 1:1]`
- Resolution: `[width × height]`
- Frame rate: `[fps]`
- Destination: `[platform or presentation context]`
- Visual sources: `[real screen recording / product model / approved UI assets / editorial graphics]`
- Audio: `[voice-over / music / interface sound / silent]`
- Subtitles: `[included in Blender / added in editing / none]`

### Narrative path

```text
[Visible product result]
→ [user action or product mechanism]
→ [second proof point]
→ [wider product context]
→ [closing result or call to action]
```

### Visual boundaries

- Show only `[approved subjects and interfaces]`.
- Exclude `[people, hands, reflections, unsupported UI, third-party notifications, or other restrictions]`.
- Keep real UI readable.
- Represent editorial transitions as editorial graphics, not as product controls.
- Do not imply an unshipped feature, interaction, or automation.

## 3. Evidence and constraints

### Source-of-truth files

| Source | File or location | What it proves | Status |
|---|---|---|---|
| Creative brief | `[brief.md]` | Intended story and constraints | `[verified / missing]` |
| Screen recording | `[screen-recording.mp4]` | Real interface and timing | `[verified / missing]` |
| Product model | `[product.glb or product.blend]` | Physical form and materials | `[verified / missing]` |
| Visual references | `[reference folder]` | Lighting, color, and composition direction | `[verified / missing]` |
| Brand assets | `[logo/font/assets]` | Approved identity elements | `[verified / not used]` |

### Facts that must be verified

- `[Product behavior shown in scene 1]`
- `[Product behavior shown in scene 2]`
- `[Exact screen text that must remain readable]`
- `[Asset license and attribution requirement]`
- `[Whether audio, subtitles, or editorial labels are required]`

### Production assumptions

| Assumption | Why it is safe for the preview | Confirmation needed before |
|---|---|---|
| `[Example: 5-second technical proof]` | Easy to retime without rebuilding the scene | Full image-sequence render |
| `[Example: generic device model]` | Exact hardware is not visible in the approved framing | Final delivery |

## 4. Master timeline

Keep this table concise. It explains the complete film without Blender implementation details.

| Time | Scene and visual action | Spoken line | On-screen emphasis | Purpose |
|---|---|---|---|---|
| `[00:00–00:04]` | **SC01:** `[Opening product action and visible result]` | `[Spoken line A]` | `[Short phrase]` | Establish the product result |
| `[00:04–00:08]` | **SC02:** `[Move from the previous composition to a specific UI result]` | `[Spoken line B]` | `[Short phrase]` | Prove the second point |
| `[00:08–00:16]` | **SC03:** `[Real interface or product demonstration]` | `[Spoken line C]` | `[Short phrase]` | Explain how it works |
| `[00:16–00:20]` | **SC04:** `[Closing composition]` | `[Closing spoken line]` | `[Call to action or product name]` | Complete the story |

## 5. Scene and spoken-line index

This is the production index shared by writing, storyboard, Blender, and editing.

| Scene | Spoken line | Concise visual description | Storyboard grid | Working file | Status |
|---|---|---|---|---|---|
| SC01 `[scene name]` | `[Spoken line A]` | `[Opening state → movement → final state]` | `storyboards/SC01-v1/SC01-storyboard-grid-v1.png` | `Blender/SC01-[slug]-v1.blend` | `[script confirmed / storyboard / approved for Blender / preview / final]` |
| SC02 `[scene name]` | `[Spoken line B]` | Starts at SC01's final composition, then `[camera/product action]` to reveal `[verified UI or product result]`. | `storyboards/SC02-v1/SC02-storyboard-grid-v1.png` | `Blender/SC02-[slug]-v1.blend` | `[script confirmed / storyboard / approved for Blender / preview / final]` |

Every spoken line should map to one primary scene. If one line spans multiple shots, list the shot transition explicitly in the master timeline.

## 6. Image2 storyboard plan and approval

Use product images and real UI references to create three deliberate frames per scene, then combine them into one numbered grid image for review.

| Scene | Frame | Image path | Product pose and camera | Lighting/background | Status |
|---|---|---|---|---|---|
| SC01 | Opening | `storyboards/SC01-v1/opening.png` | `[pose, scale, angle, crop]` | `[approved intent]` | `[draft / selected]` |
| SC01 | Hero | `storyboards/SC01-v1/hero.png` | `[pose, scale, angle, crop]` | `[approved intent]` | `[draft / selected]` |
| SC01 | Ending | `storyboards/SC01-v1/ending.png` | `[pose, scale, angle, crop]` | `[approved intent]` | `[draft / selected]` |

- Source script version: `[path/version]`
- Storyboard grid: `storyboards/SC01-v1/SC01-storyboard-grid-v1.png`
- Grid layout and panel order: `[for example, 3×1: SC01-01 → SC01-03]`
- Selected direction: `[short description]`
- Rejected alternatives: `[paths and reason]`
- User feedback: `[summary]`
- Approval status: `[storyboard_review / approved_for_blender]`
- Approval date: `[date]`

Separate panel files are working assets. Do not begin the detailed Blender implementation until the grid image is reviewed and approval status is `approved_for_blender`.

## 7. Detailed Blender scene specification

### SC01 — `[scene name]`

#### Corresponding spoken line

> `[Spoken line A]`

#### Scene objective

Start with `[opening composition]`. Let `[camera / product / hybrid rig]` own the main movement. End with `[measurable final composition]` when `[story event]` occurs.

#### Files and recovery

- Working file: `Blender/SC01-[slug]-v1.blend`
- Approved storyboard: `storyboards/SC01-v1/`
- Structural backup: `Blender/SC01-[slug]-v1-before-[change].blend`
- Screen recording: `assets/video/[recording].mp4`
- Product model: `assets/models/[model file]`
- Preview folder: `previews/SC01-[version]/`
- Image-sequence folder: `exports/SC01-[version]/frames/`
- Render status: `exports/SC01-[version]/render_status.json`

#### Output and timeline

- Aspect ratio: `[ratio]`
- Resolution: `[width × height]`
- Frame rate: `[fps]`
- Frame range: `[start–end]`
- Duration: `[(end - start + 1) / fps]`
- Render engine: `[Eevee / Cycles / rendered viewport]`
- Image master: `[JPEG / PNG / EXR]`
- Final codec: `[codec and pixel format]`

#### Movement ownership

1. Product: `[fixed / primary movement / supporting movement]`
2. Camera: `[fixed / primary movement / supporting movement]`
3. Focus target: `[screen surface or named detail]`
4. Background: `[fixed geometry with slow Shader motion / other verified behavior]`

Do not let the camera and product perform equal, unmotivated movement. Name one primary movement owner.

#### Camera and product key positions

Record actual evaluated world coordinates from Blender.

| Frame | Product rig | Camera | Look target | Focus target | Story event |
|---|---|---|---|---|---|
| `[opening]` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | Opening composition |
| `[middle]` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | Main movement |
| `[stop]` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | Product or UI event completes |
| `[final]` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | `(<x>, <y>, <z>)` | Final hold |

#### Camera and focus

- Camera object: `SC01_Camera`
- Lens: `[mm]`
- Sensor: `[width or camera type]`
- Tracking target: `SC01_LookTarget`
- Depth of field: `[on / off]`
- Focus object: `SC01_ScreenFocus`
- Aperture: `[f-stop]`
- Motion blur: `[setting and reason]`

#### Motion curve

```text
[opening frame–move start]: establish and hold
→ [move start–deceleration]: primary movement
→ [deceleration–stop]: ease into the story event
→ [stop–final]: hold the approved final composition
```

- Interpolation: `[Bezier / linear / other]`
- Handle behavior: `[AUTO_CLAMPED or measured alternative]`
- Screen playback: `[original speed / approved retime]`
- Background animation: slower than the product action

#### Lighting and background

| Role | Object | Purpose | Moves with |
|---|---|---|---|
| Product key | `SC01_Product_Key` | Reveal primary material and form | `[product / world]` |
| Front fill | `SC01_Product_Fill` | Preserve bezel and screen readability | `[product / world]` |
| Rim | `SC01_Product_Rim` | Separate product edge from background | `[product / world]` |
| Background light | `SC01_Background_Key` | Shape the physical background only | World |

- Physical background: `SC01_Physical_BackWall`
- Background Shader: `[color system and slow animation parameter]`
- Disabled legacy elements: `[duplicate wall / volume / unused light]`
- UI reflection rule: preserve legibility; do not wash out the screen.

#### Preview gates

| Gate | Evidence | Acceptance condition | Status |
|---|---|---|---|
| A | Model, screen UV, framing | Product and UI fit the delivery ratio | `[pending / pass]` |
| B | Material and lighting frames | Form reads without obscuring UI | `[pending / pass]` |
| C | Opening, middle, stop, final frames | Story events and holds align | `[pending / pass]` |
| D | Short motion proof | Easing, focus, Shader, and framing remain stable | `[pending / pass]` |

### SC02 — `[continuation scene name]`

#### Corresponding spoken line

> `[Spoken line B]`

#### Continuity contract

- Opening frame must match SC01's final approved composition.
- Reuse only verified product and UI states.
- Copy the source `.blend` to a new versioned working file.
- Create scene-specific camera, target, focus, markers, and output paths.
- Do not overwrite SC01.

#### Key differences from SC01

| Area | SC01 final | SC02 final | Reason |
|---|---|---|---|
| Camera | `[position/lens]` | `[position/lens]` | `[new visual priority]` |
| Look target | `[object/position]` | `[object/position]` | `[new focal subject]` |
| Focus target | `[object/position]` | `[object/position]` | Keep the named surface readable |
| Product | `[state]` | `[state]` | `[fixed or intentionally changed]` |
| Screen | `[verified frame/state]` | `[verified frame/state]` | Match the spoken line |

Use the same detailed subsections as SC01 for files, frame range, motion curve, lighting, previews, and export status.

## 8. Asset checklist

### Required

- [ ] Approved creative brief or measurable shot specification
- [ ] Approved Image2 storyboard grid showing opening, hero, and ending frames together
- [ ] Real screen recording or approved UI stills
- [ ] Licensed product model and textures
- [ ] One to three visual references
- [ ] Delivery ratio, resolution, fps, duration, and platform
- [ ] Audio and subtitle policy
- [ ] Brand assets only when they are actually used

### Technical checks

- [ ] No missing external files
- [ ] Texture color spaces are correct
- [ ] Screen aspect ratio and playback speed are correct
- [ ] Product scale and orientation are recorded
- [ ] Camera and focus targets are named
- [ ] Source asset licenses and attribution are recorded

## 9. Preview and export gates

### Representative frames

| Frame | Preview file | What was checked | Result |
|---|---|---|---|
| `[opening]` | `previews/[scene]/[opening].png` | First composition and UI | `[pass / revise]` |
| `[middle]` | `previews/[scene]/[middle].png` | Movement direction and focus | `[pass / revise]` |
| `[stop]` | `previews/[scene]/[stop].png` | Story event alignment | `[pass / revise]` |
| `[final]` | `previews/[scene]/[final].png` | Final hold and crop | `[pass / revise]` |

### Image-sequence master

- Expected frame count: `[count]`
- Actual frame count: `[count]`
- Dimensions: `[width × height]`
- Missing or duplicate frames: `[none / details]`
- Validation result: `[pass / fail]`

### Final video

- Video file: `exports/[scene-version]/[scene].mp4`
- Thumbnail: `exports/[scene-version]/[scene]-thumbnail.jpg`
- Codec: `[codec]`
- Frame rate: `[fps]`
- Duration: `[seconds]`
- File size: `[size]`
- Audio: `[included / none]`
- Subtitles: `[included / editing-stage / none]`
- Quality compromise: `[none / describe]`

## 10. Production status and handoff

Use explicit states:

```text
Draft script
→ Script confirmed
→ Image2 storyboard draft
→ Storyboard approved for Blender
→ Technical still preview
→ Short motion proof
→ Approved for full render
→ Image sequence complete and validated
→ Video encoded and verified
→ Script synchronized
→ Final handoff complete
```

Before handoff, confirm:

- [ ] The master timeline matches the scene index.
- [ ] The selected storyboard matches the script and has explicit approval.
- [ ] The scene index matches the detailed Blender sections.
- [ ] The detailed parameters match the saved `.blend`.
- [ ] Preview, image-sequence, video, and status paths exist.
- [ ] Product behavior and visible UI are backed by real source assets.
- [ ] The user can tell what is complete, what is pending, and what requires approval.
