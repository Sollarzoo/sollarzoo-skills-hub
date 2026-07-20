[English](README.md) | 简体中文

# sollarzoo-skills-hub

一个 [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) 集合 —— 打包好的、可复用的指令集，用于扩展 Claude Code 的专项工作流能力。

## 技能列表

### [blender-product-scene-video](blender-product-scene-video/SKILL.md)

根据创意脚本、3D 模型、贴图、屏幕录屏和视觉参考，构建并交付可复用的 Blender 产品场景动画。

适用场景：需要检查或初始化 Blender 场景、编写缺失的分镜脚本、加载并摆放产品模型、配置 PBR 材质和视频贴图、设计灯光/背景/程序化 Shader 动画、为相机或产品制作动画、渲染并校验图像序列、编码最终 MP4 视频、诊断闪烁/模糊/构图/渲染耗时等问题,或为后续场景记录制作参数。

该技能将一个产品短片创意转化为四个同步交付物:

1. 一份已确认的分镜脚本;
2. 一个可回退的 `.blend` 场景文件;
3. 一套完整且经过校验的图像序列;
4. 一段可播放的最终视频,附带缩略图和制作记录。

**目录结构:**

| 路径 | 说明 |
|---|---|
| `SKILL.md` | 入口文档 —— 目标、工作流与质量准则 |
| `references/intake-and-script.md` | 如何收集需求并起草分镜脚本 |
| `references/scene-build-sop.md` | Blender 场景搭建的标准操作流程 |
| `references/render-export-qc.md` | 渲染、导出与质量检查清单 |
| `references/troubleshooting.md` | 闪烁、模糊、速度错误、灯光不足、构图、渲染缓慢等问题的排查方法 |
| `assets/scene-brief-template.md` | 用户没有可用脚本时,用于起草分镜脚本的模板 |
| `scripts/init_project.py` | 初始化场景工作目录(源素材、预览、图像序列、视频、日志) |
| `scripts/validate_image_sequence.py` | 校验渲染出的图像序列(数量、尺寸) |
| `scripts/encode_avfoundation.swift` | macOS 上基于 AVFoundation 的编码器,将图像序列合成为 MP4 |

## 如何使用这些技能

本仓库中的技能遵循标准的 Claude Agent Skills 格式:一个带 YAML frontmatter(`name`、`description`)的 `SKILL.md`,配合 `references/`、`assets/`、`scripts/` 等支持目录。将技能目录放入项目级或用户级的 `skills/` 目录下,即可让 Claude Code 发现并调用它。

## 许可证

[MIT](LICENSE) © 2026 sollarzoo
