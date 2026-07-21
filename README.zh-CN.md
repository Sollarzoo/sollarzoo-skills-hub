[English](README.md) | 简体中文

# sollarzoo-skills-hub

一个 [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) 集合 —— 打包好的、可复用的指令集，用于扩展 Claude Code 的专项工作流能力。

## 技能列表

### [daily-report](daily-report/SKILL.md)

| 元信息 | 内容 |
|---|---|
| 开发者 | [`sollarzoo`](https://github.com/Sollarzoo) |
| 版本 | `5.3.1` |
| 反馈联系 | 微信：`sollarzoo` |

根据仓库活动和对话上下文生成以任务为单位的 Markdown 日报。该技能可使用
Toggl Track API v9 作为工时证据，在写入任务工时前强制人工确认，生成
PAL 兼容日报、重建 ROI 与任务回链，并将已确认的任务累计工时幂等同步到
Notion 任务数据库。

**目录结构:**

| 路径 | 说明 |
|---|---|
| `SKILL.md` | 完整的日报流程和失败恢复规则 |
| `config.example.json` | 设备、PAL、时区和 Notion 设置的公开安全模板 |
| `toggl_track.py` | 不泄露凭据的 Toggl Track API v9 客户端 |
| `helpers.py` | 主题、已有日报和 problem-space 辅助函数 |
| `references/getting-started.md` | 七步初始化与 Toggl API 配置指南 |
| `references/toggl-track-notion-sync.md` | 凭据、任务匹配与 Notion 幂等同步协议 |
| `tests/` | helpers 与 Toggl 工时聚合测试 |

**首次使用：**按照
[`references/getting-started.md`](daily-report/references/getting-started.md)
安装完整 Skill，从 `config.example.json` 创建私有配置，把 Toggl API Token
保存到 Git 忽略的 `.env` 或 macOS Keychain，验证真实 API 响应，连接
Notion，然后运行第一份需要人工确认工时的日报。

**最新版本 — v5.3.1（2026-07-20）：**新增七步首次使用指南、公开安全配置
模板、明确的 Toggl Token 配置与验证步骤，以及可配置的 Notion 数据库和字段。
完整版本历史见
[`daily-report/SKILL.md`](daily-report/SKILL.md)。

### [blender-product-scene-video](blender-product-scene-video/SKILL.md)

| 元信息 | 内容 |
|---|---|
| 开发者 | [`sollarzoo`](https://github.com/Sollarzoo) |
| 版本 | `1.5.1` |
| 反馈联系 | 微信：`sollarzoo` |

根据已确认的创意脚本、产品图片、3D 模型、贴图、屏幕录屏和视觉参考，
规划故事板、搭建 Blender 场景并交付可复用的产品动画。

制作流程分为四个面向用户的阶段：

1. 将旁白拆成可追溯的视觉节拍，并核验每个真实 UI 画面的证据；
2. 生成一张带编号和技术标注的 Image2 草图宫格故事板并取得明确确认；
3. 按已确认故事板搭建 Blender 场景、灯光、材质、模型和动画；
4. 渲染图像序列、编码视频、完成质量检查与制作记录交付。

故事板确认是硬门槛：用户没有确认覆盖全片的宫格图之前，不进入 Blender
正式制作。每格必须包含对应旁白、设计理由、运动轨迹、相机/手机轴、灯光方向、
转场方式和 UI 证据。

**目录结构:**

| 路径 | 说明 |
|---|---|
| `SKILL.md` | 入口文档 —— 目标、工作流与质量准则 |
| `references/intake-and-script.md` | 如何收集需求并起草分镜脚本 |
| `references/storyboard-sop.md` | Image2 故事板生成、宫格拼接、确认与回退规则 |
| `references/scene-build-sop.md` | Blender 场景搭建的标准操作流程 |
| `references/render-export-qc.md` | 渲染、导出与质量检查清单 |
| `references/troubleshooting.md` | 闪烁、模糊、速度错误、灯光不足、构图、渲染缓慢等问题的排查方法 |
| `assets/scene-brief-template.md` | 用户没有可用脚本时,用于起草分镜脚本的模板 |
| `assets/storyboard-template.md` | 故事板索引、确认记录与 Blender 交接模板 |
| `scripts/init_project.py` | 初始化场景工作目录(源素材、预览、图像序列、视频、日志) |
| `scripts/validate_image_sequence.py` | 校验渲染出的图像序列(数量、尺寸) |
| `scripts/encode_avfoundation.swift` | macOS 上基于 AVFoundation 的编码器,将图像序列合成为 MP4 |

**最新版本 — v1.5.1：**新增逐句旁白节拍、全片连续性评审、按原始文件名
引用的真实 UI 证据门、带运动/坐标轴/灯光图例的草图故事板、明确的剪辑转场和
设计理由。项目专属视觉创意保留在项目脚本中，不写成通用 Skill 默认方案。

## 如何使用这些技能

本仓库中的技能遵循标准的 Claude Agent Skills 格式:一个带 YAML frontmatter(`name`、`description`)的 `SKILL.md`,配合 `references/`、`assets/`、`scripts/` 等支持目录。将技能目录放入项目级或用户级的 `skills/` 目录下,即可让 Claude Code 发现并调用它。

## 许可证

[MIT](LICENSE) © 2026 sollarzoo
