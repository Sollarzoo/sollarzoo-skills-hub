English | [简体中文](README.zh-CN.md)

# sollarzoo-skills-hub

A collection of [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — packaged, reusable instructions that extend Claude Code with specialized workflows.

## Skills

### [daily-report](daily-report/SKILL.md)

| Metadata | Value |
|---|---|
| Developer | [`sollarzoo`](https://github.com/Sollarzoo) |
| Version | `5.3.1` |
| Feedback | WeChat: `sollarzoo` |

Generate task-oriented Markdown daily reports from repository activity and conversation
context. The skill can use Toggl Track API v9 as time evidence, requires human
confirmation before finalizing task hours, writes PAL-compatible reports, rebuilds
ROI/backlinks, and idempotently synchronizes confirmed cumulative hours to a Notion
task database.

**Contents:**

| Path | Purpose |
|---|---|
| `SKILL.md` | Complete daily-report workflow and failure-recovery rules |
| `config.example.json` | Public-safe template for device, PAL, timezone, and Notion settings |
| `toggl_track.py` | Secret-safe Toggl Track API v9 client |
| `helpers.py` | Theme, existing-report, and problem-space helpers |
| `references/getting-started.md` | Seven-step initialization and Toggl API setup guide |
| `references/toggl-track-notion-sync.md` | Credential, matching, and idempotent Notion sync protocol |
| `tests/` | Unit tests for helpers and Toggl time aggregation |

**First run:** follow
[`references/getting-started.md`](daily-report/references/getting-started.md) to
install the full Skill, create a private config from `config.example.json`,
store the Toggl API token in a Git-ignored `.env` or macOS Keychain, verify the
live API response, connect Notion, and run the first confirmed report.

**Latest release — v5.3.1 (2026-07-20):** added the seven-step first-run guide,
public-safe configuration template, explicit Toggl token setup and verification,
and configurable Notion database/property fields. See the complete version
history in [`daily-report/SKILL.md`](daily-report/SKILL.md).

### [blender-product-scene-video](blender-product-scene-video/SKILL.md)

| Metadata | Value |
|---|---|
| Developer | [`sollarzoo`](https://github.com/Sollarzoo) |
| Version | `1.5.1` |
| Feedback | WeChat: `sollarzoo` |

Plan, storyboard, build, and deliver reusable Blender product-scene animations
from an approved creative script, product images, 3D model, textures, screen
recording, and visual references.

The production workflow has four user-facing stages:

1. split the narration into script-traceable visual beats and verify real UI evidence;
2. generate one numbered, annotated rough-sketch storyboard grid and obtain explicit approval;
3. build the approved Blender scene, lighting, materials, models, and animation;
4. render an image sequence, encode the video, run QC, and hand off production records.

Storyboard approval is a hard gate: Blender production does not begin until the
user approves the complete numbered grid image. Every panel carries its exact
narration, design reason, motion path, camera/phone axis, lighting direction,
transition, and evidence reference.

**Contents:**

| Path | Purpose |
|---|---|
| `SKILL.md` | Entry point — outcome, workflow, and quality rules |
| `references/intake-and-script.md` | How to gather requirements and draft a shot specification |
| `references/storyboard-sop.md` | Image2 storyboard generation, grid assembly, approval, and rollback rules |
| `references/scene-build-sop.md` | Standard operating procedure for building the Blender scene |
| `references/render-export-qc.md` | Render, export, and quality-control checklist |
| `references/troubleshooting.md` | Fixes for flicker, blur, wrong speed, weak lighting, framing, slow renders |
| `assets/scene-brief-template.md` | Template for drafting a shot specification when none exists |
| `assets/storyboard-template.md` | Storyboard index, approval record, and Blender handoff template |
| `scripts/init_project.py` | Scaffolds a scene workspace (source assets, previews, sequences, videos, logs) |
| `scripts/validate_image_sequence.py` | Validates a rendered image sequence (count, dimensions) |
| `scripts/encode_avfoundation.swift` | macOS AVFoundation encoder for turning an image sequence into an MP4 |

**Latest release — v1.5.1:** added clause-level narration beats, complete-film
continuity review, real-UI evidence gates using exact filenames, rough-sketch
storyboards with motion/axis/light legends, explicit edit transitions, and
design rationale. Project-specific visual concepts remain in project scripts
instead of becoming reusable skill defaults.

## Using these skills

Skills in this repo follow the standard Claude Agent Skills format: a `SKILL.md` with YAML frontmatter (`name`, `description`) plus supporting `references/`, `assets/`, and `scripts/`. Install a skill by placing its directory under your project's or user's `skills/` directory so Claude Code can discover and invoke it.

## License

[MIT](LICENSE) © 2026 sollarzoo
