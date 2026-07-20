# Render, export, and QC SOP

## Contents

1. Apply the image-first rule
2. Choose quality route
3. Prepare output
4. Export sequence
5. Validate
6. Select a platform encoder
7. Encode on macOS
8. Encode on Windows
9. Add audio
10. Final QC and handoff

## 1. Apply the image-first rule

Use this production state machine:

```text
Blender animation
  → numbered image sequence
  → sequence validation
  → representative-frame inspection
  → platform encoder
  → video/thumbnail verification
```

The image sequence is the render master. The MP4 is a delivery derivative.

Reasons:

- an interrupted render retains valid completed frames;
- a bad frame can be replaced without rerendering the entire scene;
- fps, bitrate, codec, container, and audio can change without reopening Blender;
- frame count and duration can be verified before encoding;
- macOS and Windows can consume the same render master.

Exceptions:

- a static scene stops after the still image;
- a disposable 1–3 second viewport test may render directly to video;
- real-time capture/live streaming uses a separate capture workflow.

Do not make direct-to-video the default for a final animation.

## 2. Choose the route

| Route | Use for | Typical trade-off |
|---|---|---|
| Rendered viewport | Fast look review and social preview | Fast; viewport-dependent |
| Eevee render | Final product video with moderate reflections/Shader | Balanced |
| Cycles render | Hero frames and physically demanding materials | Slowest |

Agree on whether “final” means fast review quality or hero quality. Never imply that viewport output is a full Cycles render.

## 3. Prepare output

Use a new versioned directory:

```text
exports/<scene-version>/
├── frames/
├── render_status.json
├── <scene>-<width>x<height>.mp4
└── <scene>-thumbnail.jpg
```

Do not overwrite a previous approved export. Record:

- width and height;
- resolution percentage;
- fps;
- start/end frame;
- image format and quality;
- render engine/samples;
- expected frame count: `end - start + 1`;
- expected duration: `frame_count / fps`.

Use JPEG for fast review and PNG/EXR when alpha, grading latitude, or lossless intermediates are required.

## 4. Export the image sequence

For Blender MCP rendered-viewport export:

1. find a real `VIEW_3D` window/area/region;
2. switch it to camera view and rendered shading;
3. hide overlays and gizmos;
4. set frame range, resolution, fps, image format, and a unique filepath;
5. write `render_status.json` as `scheduled`;
6. register a Blender timer so the MCP call returns instead of timing out;
7. change status to `rendering`, call `bpy.ops.render.opengl(animation=True, view_context=True)`, then write `images_complete` or `error`;
8. monitor frame count from the shell and report progress.

For final Eevee/Cycles export, use `bpy.ops.render.render(animation=True)` or the Render Animation UI command. The same versioned folder and status rules apply.

Do not use background Blender for viewport export because it has no interactive `VIEW_3D`. Use standard render operators in background mode.

## 5. Validate the sequence

Run:

```bash
python3 scripts/validate_image_sequence.py frames \
  --expected-count 1740 --start 1 --end 1740 \
  --width 1080 --height 1920
```

The validator checks sorting, numbering gaps, duplicates, and JPEG/PNG dimensions. Also inspect:

- first frame;
- a typing/action frame;
- the movement stop frame;
- a late feature frame;
- final frame.

Play or scrub a short continuous span to check Shader shimmer, Z-fighting, DOF pulsing, light popping, and camera easing.

Do not encode if validation fails.

## 6. Select a platform encoder

Detect instead of assuming:

| Platform | Primary | Secondary | Account |
|---|---|---|---|
| macOS | bundled AVFoundation encoder | FFmpeg with VideoToolbox or `libx264` | none |
| Windows | FFmpeg with `libx264` | supported GPU encoder or Blender VSE | none |
| Linux | FFmpeg with `libx264` | supported GPU encoder | none |

Before encoding, record:

- operating system and architecture;
- encoder version;
- available codecs;
- input filename pattern and start number;
- width, height, fps, and expected duration;
- whether audio and subtitles are required.

Installing Xcode Command Line Tools or another encoder changes the machine. Explain what is needed and obtain user/host approval. Treat FFmpeg as a manual user prerequisite: detect it, provide the official installation instructions, wait for the user to finish, and verify it afterward. Do not download, extract, package-manage, or modify `PATH` for FFmpeg automatically. Never request a password; let the user and OS handle any administrator prompt.

## 7. Encode on macOS

### Preferred: bundled AVFoundation

Compile once:

```bash
xcrun swiftc -O scripts/encode_avfoundation.swift -o scripts/encode_avfoundation
```

Encode:

```bash
scripts/encode_avfoundation frames output.mp4 thumbnail.jpg 1080 1920 30 12000000
```

This produces silent H.264 video. Audio and subtitles must be added later unless explicitly included in a separate edit.

If `xcrun` or Swift is unavailable, ask the user whether to install Apple Command Line Tools or manually install FFmpeg instead. Do not download an unverified precompiled encoder.

### macOS FFmpeg alternative

If installed:

```bash
ffmpeg -framerate 30 -start_number 1 -i 'SC01_%04d.jpg' \
  -c:v h264_videotoolbox -b:v 12M -pix_fmt yuv420p \
  -movflags +faststart output.mp4
```

If VideoToolbox fails, use the portable software fallback:

```bash
ffmpeg -framerate 30 -start_number 1 -i 'SC01_%04d.jpg' \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -movflags +faststart output.mp4
```

## 8. Encode on Windows

### Install and verify FFmpeg

Check:

```powershell
ffmpeg -version
ffprobe -version
```

If missing, send the user to the official download page:

<https://ffmpeg.org/download.html#build-windows>

FFmpeg publishes source code and links to Windows executable-build providers. FFmpeg installation is a user-operated step:

1. Open the official download page.
2. Choose one of the Windows build providers linked by FFmpeg.
3. Download the appropriate Windows archive.
4. Extract it to a stable user-selected directory, for example `C:\Tools\ffmpeg`.
5. Add its `bin` directory, for example `C:\Tools\ffmpeg\bin`, to the Windows user `PATH`.
6. Close and reopen PowerShell.
7. Run `ffmpeg -version` and `ffprobe -version`.
8. Tell Codex that both commands now succeed.

Codex must wait at this gate. It must not download the archive, select a third-party build on the user's behalf, edit `PATH`, or claim installation succeeded. No FFmpeg account or API key is required.

### Reliable default: software H.264

From the frames directory:

```powershell
ffmpeg -framerate 30 -start_number 1 -i "SC01_%04d.jpg" `
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p `
  -movflags +faststart "SC01-output.mp4"
```

Notes:

- replace `30` with the Blender scene fps;
- replace `1` with the first frame number;
- match `%04d` to the actual zero-padding;
- PowerShell uses the backtick for line continuation;
- use the same command on one line in Command Prompt;
- inside a Windows `.bat` file, escape `%` as `%%04d`;
- quote every path containing spaces.

For a faster review encode, use `-preset veryfast -crf 22`. For a higher-quality software encode, use `-preset medium -crf 17` or `18`. Do not change fps to make encoding faster.

### Optional Windows hardware encoders

Inspect the installed build:

```powershell
ffmpeg -hide_banner -encoders | findstr /I "h264_nvenc h264_qsv h264_amf"
```

Possible mappings:

| Hardware | Encoder |
|---|---|
| NVIDIA | `h264_nvenc` |
| Intel Quick Sync | `h264_qsv` |
| AMD | `h264_amf` |

Use only an encoder shown by the command. Test 30–90 frames before encoding the full sequence. If the hardware command fails or produces invalid output, fall back to `libx264`.

A broadly compatible bitrate-based test is:

```powershell
ffmpeg -framerate 30 -start_number 1 -i "SC01_%04d.jpg" `
  -c:v h264_nvenc -b:v 12M -pix_fmt yuv420p `
  -movflags +faststart "SC01-hardware-test.mp4"
```

Replace `h264_nvenc` only with a confirmed available encoder. Encoder-specific quality flags vary by FFmpeg build, so inspect `ffmpeg -h encoder=<name>` before tuning.

### Windows fallback without standalone FFmpeg

Use Blender’s Video Sequencer:

1. create a new scene or backup;
2. add the numbered images as one image sequence strip;
3. set scene fps and frame range to match the render master;
4. set output to FFmpeg Video, MPEG-4 container, H.264 video;
5. render the animation to a new versioned output path;
6. verify duration and orientation.

This is more manual and less convenient for repeated encoding, but it avoids rerendering the 3D scene. Do not import the frames into the original production scene without a backup.

## 9. Add audio

The image sequence and bundled AVFoundation encoder produce silent video. Ask whether the delivery needs original screen audio, music, voiceover, or no audio.

With FFmpeg:

```bash
ffmpeg -i silent-video.mp4 -i audio.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k \
  -shortest -movflags +faststart final-with-audio.mp4
```

Do not use `-shortest` blindly when the audio must extend beyond the image sequence. Confirm the intended end behavior. Subtitles should normally be added in the editing stage unless the user explicitly asks to burn them in.

## 10. Final QC and handoff

Verify:

- [ ] frame count and duration match;
- [ ] pixel dimensions and orientation match delivery;
- [ ] no missing/duplicate frames;
- [ ] UI playback speed matches source;
- [ ] focus stays on screen;
- [ ] product reaches and holds the intended stop frame;
- [ ] background remains stable relative to world;
- [ ] Shader movement is continuous;
- [ ] no blank, black, upside-down, or rotated output;
- [ ] file opens and thumbnail is upright;
- [ ] codec and pixel format are compatible with the destination platform;
- [ ] audio presence/absence matches the request;
- [ ] final file size is plausible;
- [ ] script and `.blend` match.

Verify with `ffprobe` when available:

```bash
ffprobe -v error -show_entries \
  stream=codec_name,width,height,pix_fmt,r_frame_rate,duration \
  -show_entries format=duration,size -of json output.mp4
```

On macOS without `ffprobe`, use AVFoundation/QuickTime metadata and open the generated thumbnail. Do not treat file existence alone as successful encoding.

Deliver file links and a compact report. State image count, video dimensions, fps, duration, codec, pixel format, file size, audio/subtitle status, render route, encoder path, and any remaining limitation.
