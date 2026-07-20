English | [简体中文](README.zh-CN.md)

# sollarzoo-skills-hub

A collection of [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — packaged, reusable instructions that extend Claude Code with specialized workflows.

## Skills

### [blender-product-scene-video](blender-product-scene-video/SKILL.md)

Build and deliver reusable Blender product-scene animations from a creative script, 3D model, textures, screen recording, and visual references.

Use it when Claude needs to inspect or initialize a Blender scene, write a shot script, position a product model, configure PBR materials and video textures, design lighting/background/Shader animation, animate cameras or products, render image sequences, encode a final MP4, diagnose rendering problems (flicker, blur, framing, render time), or document production settings for later scenes.

The skill turns a product-film idea into four synchronized deliverables:

1. an approved shot specification
2. a reversible `.blend` scene
3. a validated image sequence
4. a final video plus thumbnail and production record

**Contents:**

| Path | Purpose |
|---|---|
| `SKILL.md` | Entry point — outcome, workflow, and quality rules |
| `references/intake-and-script.md` | How to gather requirements and draft a shot specification |
| `references/scene-build-sop.md` | Standard operating procedure for building the Blender scene |
| `references/render-export-qc.md` | Render, export, and quality-control checklist |
| `references/troubleshooting.md` | Fixes for flicker, blur, wrong speed, weak lighting, framing, slow renders |
| `assets/scene-brief-template.md` | Template for drafting a shot specification when none exists |
| `scripts/init_project.py` | Scaffolds a scene workspace (source assets, previews, sequences, videos, logs) |
| `scripts/validate_image_sequence.py` | Validates a rendered image sequence (count, dimensions) |
| `scripts/encode_avfoundation.swift` | macOS AVFoundation encoder for turning an image sequence into an MP4 |

## Using these skills

Skills in this repo follow the standard Claude Agent Skills format: a `SKILL.md` with YAML frontmatter (`name`, `description`) plus supporting `references/`, `assets/`, and `scripts/`. Install a skill by placing its directory under your project's or user's `skills/` directory so Claude Code can discover and invoke it.

## License

[MIT](LICENSE) © 2026 sollarzoo
