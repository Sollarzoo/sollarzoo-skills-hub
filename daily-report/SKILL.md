---
name: daily-report
description: >
  把今天的开发工作整理成一份以任务为单位的 Markdown 日报。
  每个任务记录完整流程、遇到的问题、解决方式与经验沉淀。
  v5.3 起：写本地项目 docs/daily/{date}-{theme}.md（所有设备）+
  PAL-Obsidian/8-日报/{user}/{date}-{theme}.md（仅 Mac mini 本机直写；
  MacBook 等非 PAL 主机必须通过 SSH 同步到 Mac mini，
  严禁写入本机 PAL-Obsidian 目录）；
  从 Toggl Track API v9 获取工时草案，经用户确认后写入 task_hours，
  并将任务累计确认工时幂等同步到 Notion 任务池的“工时(h)”字段；
  收尾时调用 pal-memory 按 problem-space 切片沉淀到 9-memory。
  触发示例："帮我写今天的日报" / "总结今天的工作" / "/daily-report"
---

# Daily Report Skill

## Skill metadata

- Developer: `sollarzoo`
- Author: [sollarzoo](https://github.com/Sollarzoo)
- Version: `5.3.1`
- Feedback WeChat: `sollarzoo`

## Version history

| Version | Date | Changes |
|---|---|---|
| `5.3.1` | 2026-07-20 | Add a seven-step first-run guide, public-safe configuration template, Toggl token setup and verification instructions, and configurable Notion database fields. |
| `5.3.0` | 2026-07-20 | Add Toggl Track API v9 time evidence, `.env`/Keychain credential handling, mandatory task-hour confirmation, and idempotent cumulative-hour synchronization to Notion. |
| `5.2.0` | 2026-06-21 | Establish local + PAL host report delivery, dual-route SSH recovery, daily index rebuilding, task ROI derivation, and task backlinks. |
| `5.1.0` | Historical | Introduce themed filenames, incremental daily-report updates, and remove the legacy Notion page/body synchronization flow. |

以任务为单位整理今日开发工作，沉淀流程经验。

---

## 首次使用：从这里开始

如果私有配置不存在、Toggl 尚未验证，或用户询问“如何初始化/配置 API”，
必须先完整读取 [references/getting-started.md](references/getting-started.md)，
按以下顺序执行，不要直接跳到日报生成：

1. 安装完整 Skill 目录；
2. 从 `config.example.json` 创建仓库外的私有 `config.json`；
3. 填写设备、用户、PAL 路径、时区和 Notion 字段；
4. 从 Toggl Profile 获取 API Token；
5. 将 Token 保存到被 Git 忽略的 `.env` 或 macOS Keychain；
6. 使用 `toggl_track.py` 做真实 API 验证；
7. 连接并只读验证 Notion 后，运行首次日报。

首次初始化时持续显示：

```text
初始化进度：步骤 4/7 — 配置 Toggl Track
已完成：Skill 安装、私有配置、PAL 路径
当前：保存并验证 API Token
下一步：验证 Notion 数据库
然后：生成首次日报并确认 task_hours
```

只有 Toggl 返回 `ok: true` 才能宣告 API 配置成功。只有 Notion schema 和目标
任务页均复查成功，才能宣告 Notion 工时同步可用。任何 Token 都不得出现在
聊天、日志、日报、Git diff 或公开配置中。

---

## 触发条件

- `帮我写今天的日报`
- `总结今天的工作`
- `生成日报`
- `/daily-report`
- 完成一个完整任务、阶段性长周期任务或跨多轮排查后，Agent 可自动触发本 skill 进行增量日报写入。

## 自动执行策略

- 完整任务或长周期阶段结束后，Agent 应自动执行本 skill，无需再次征得用户同意。
- 自动执行时默认采用增量更新：读取当天已有 `docs/daily/<YYYY-MM-DD>.md`，保留已有内容，补充或修正本次任务条目，并同步更新 `## Agent 快速读取摘要`。
- 自动执行的首要目标是“不遗漏重要内容”：宁可多做一次遗漏扫描，也不要只根据最终 diff 写日报。
- 若本次任务没有产生代码 diff，也要记录重要的排查过程、决策依据、被否定的方案和文档/规则变化。
- 只有在用户明确要求“不要写日报 / 暂停日报 / 这次不用记录”时，才跳过自动写入。

---

## 执行流程

### Step 0 — 读取设备配置 + 用户身份注册

读取配置：

```bash
cat ~/.claude/skills/daily-report/config.json 2>/dev/null
```

**判断分支**：

| 状态 | 行动 |
|------|------|
| config.json 完整（含 device_id / user_id / display_name / pal_base_url / pal_base_path / pal_local_path） | 直接读取，跳到 Step 1 |
| config.json 存在但 user_id 缺失或为 `"unregistered"` | 跳到 §0d **用户身份注册** |
| config.json 不存在 | 依次执行 §0a → §0b → §0c → §0d → §0e |

#### 0a. 优先：检查 `$PAL_ROOT` 环境变量

适合多机器统一管理的高级用户：

```bash
if [ -n "$PAL_ROOT" ] && [ -d "$PAL_ROOT/PAL-Obsidian/8-日报" ]; then
  PAL_BASE_PATH="$PAL_ROOT/PAL-Obsidian/8-日报"
  echo "✓ 从 \$PAL_ROOT 自动解析：$PAL_BASE_PATH"
fi
```

#### 0b. 次选：自动搜索本机的 PAL 仓库

适合大多数普通用户。在常见父目录下搜 `CLAUDE.md`，再验证内容确属 PAL：

```bash
if [ -z "$PAL_BASE_PATH" ]; then
  PAL_GUESS=$(find ~/Documents ~/code ~/work ~/dev ~/Projects /opt 2>/dev/null \
    -maxdepth 4 -name "CLAUDE.md" \
    -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/99-legacy/*" 2>/dev/null | \
    xargs grep -l "Product[- ]Agentic[- ]Loop\|让产品迭代通过 AI 自动化" 2>/dev/null | \
    head -1 | xargs dirname 2>/dev/null)

  if [ -n "$PAL_GUESS" ] && [ -d "$PAL_GUESS/PAL-Obsidian/8-日报" ]; then
    PAL_BASE_PATH="$PAL_GUESS/PAL-Obsidian/8-日报"
    echo "✓ 自动检测到 PAL 仓库：$PAL_GUESS"
    echo "建议 pal_base_path = $PAL_BASE_PATH（按 Y 确认）"
  fi
fi
```

#### 0c. 兜底：手动输入

若以上两步均未得到路径，向用户收集 `pal_base_path`（PAL v5 推荐：`<pal-root>/PAL-Obsidian/8-日报`，**不含**用户子目录，由注册流程追加）。

#### 0d. **用户身份注册**

> ⚠️ **首次使用时必做**。skill 区分多用户，每个用户的日报落地到独立子目录。

向用户展示选项：

```
请选择当前使用者（首次注册，写入 config.json 后不再询问）：

  1) 松松
  2) 苏苏
  3) 其他用户（自定义 user_id / display_name）

请输入选项编号 [1/2/3]：
```

根据选择填充字段：

| 选项 | user_id | display_name |
|------|---------|--------------|
| 1 | `松松` | `松松` |
| 2 | `苏苏` | `苏苏` |
| 3 | 用户输入 | 用户输入 |

> v5.3 只恢复“任务累计工时”同步，不恢复旧版日报正文/页面同步。
> `notion_user_id` 仍只为兼容旧配置保留；工时同步按任务卡
> `notion_page_id` 定位。

#### 0e. 派生 `pal_local_path` + 写入 config.json

```
pal_local_path = ${pal_base_path}/${user_id}
```

即：`<pal-root>/PAL-Obsidian/8-日报/<user_id>/`，每位用户独占子目录。

完整 config.json schema（公开模板见 `config.example.json`）：

```json
{
  "device_id": "mbp",
  "user_id": "松松",
  "display_name": "松松",
  "notion_user_id": "ebaac5f5-5d2e-4ed7-8187-b3e88d1e1468",
  "pal_base_url": "http://localhost:3000",
  "pal_base_path": "/Users/xxx/Documents/Product-Agentic-Loop/PAL-Obsidian/8-日报",
  "pal_local_path": "/Users/xxx/Documents/Product-Agentic-Loop/PAL-Obsidian/8-日报/松松",
  "timezone": "Asia/Shanghai",
  "notion_database_id": "replace-with-your-notion-database-id",
  "notion_data_source_id": "",
  "notion_title_property": "问题描述",
  "notion_hours_property": "工时(h)"
}
```

（`notion_user_id` 保留在 schema 中以兼容旧版本；v5.3 工时同步不读取它。）

用 Write 工具写入 `~/.claude/skills/daily-report/config.json` 后继续。

#### 0f. 设备角色判断（PAL 主机 vs 工作机）

读取完 config.json 后，立即执行以下判断，设置运行时标志 `IS_PAL_HOST`：

```
IS_PAL_HOST = (device_id == "macmini")
```

| device_id | IS_PAL_HOST | PAL-Obsidian 本地写 | SSH 同步 |
|-----------|-------------|-------------------|---------|
| `"macmini"` | ✅ true | 允许（Step 5a 正常执行） | 可选 |
| 其他（如 `"mbp"`） | ❌ false | **⛔ 禁止** | **必须**（Step 5b 强制） |

> **架构背景**：PAL-Obsidian 目录在 MacBook 和 Mac mini 上均被 `.gitignore`，实际同步通过 Obsidian Remotely Save (OSS) 完成。MacBook 上写入本机 PAL-Obsidian 并不等于同步到 Mac mini，只会造成"写了但没用"的假象。因此非 Mac mini 设备**禁止**写入本机 PAL-Obsidian，唯一合法路径是 SSH 直写 Mac mini。

如果你在 MacBook 上运行且不确定 Mac mini 是否在线，在开始 Step 5 之前**必须按顺序探活 LAN + Tailscale 两条通道**，把第一个通的写进运行时变量 `PAL_SSH_HOST`，**两条都不通才能判定为离线**：

```bash
PAL_SSH_HOST=""
for host in palhost-lan palhost-ts; do
  if ssh -o ConnectTimeout=8 -o BatchMode=yes "$host" "echo ok" 2>/dev/null | grep -q ok; then
    PAL_SSH_HOST="$host"
    echo "✓ Mac mini 在线（通道：$host）"
    break
  else
    echo "✗ $host 不通，尝试下一通道..."
  fi
done

if [ -z "$PAL_SSH_HOST" ]; then
  echo "⚠ Mac mini 离线（palhost-lan 与 palhost-ts 均不可达），将走 pal-sync: pending 流程"
fi
```

**通道选择策略**：
- `palhost-lan`（直连 LAN）速度最快，优先尝试
- `palhost-ts`（Tailscale 隧道）跨网络可达，作为 fallback —— 出差 / 异网 / VPN 切换等场景必备
- **禁止**只试 LAN 就判定离线；这会在跨网络场景下误报，导致明明可以同步的日报被错误地积压成 pending

**后续所有 SSH 命令（Step 5b / 5d / 5.6）必须使用 `$PAL_SSH_HOST` 变量**，不要硬编码 `palhost-lan`。skill 内所有示例都已经统一改用 `$PAL_SSH_HOST`；如果你在执行时看到硬编码 `palhost-lan`，那是历史 bug，必须修复后再运行。

只有 `PAL_SSH_HOST` 为空（两条通道都失败）时才按失败矩阵处理（`pal-sync: pending` 标记），**绝不**回退到本机 PAL-Obsidian 写入。

---

#### 运行时切换用户（可选）

若同台机器多人共用，可设置环境变量临时覆盖：

```bash
PAL_USER=苏苏 /daily-report
```

skill 读到 `$PAL_USER` 时按以下规则解析：
- 若 user_id 是已知用户（松松 / 苏苏）→ 自动填充对应 display_name
- 否则要求用户在对话中临时提供 display_name

派生 `pal_local_path = ${pal_base_path}/${PAL_USER}` 用于本次写入，**不持久化**修改 config.json。

> **路径隐私**：`config.json` 位于 `~/.claude/skills/daily-report/`（用户家目录），**本身就不在任何 git 仓库内**，不会被 commit，无需额外 gitignore 配置。每台设备独立维护。
>
> **跨用户写入隔离**：PAL `PAL-Obsidian/8-日报/<user_id>/` 子目录入库到 PAL git 仓库，多用户的日报互不覆盖。

### Step 1 — 收集原始信息（并行执行）

**1a. 当前仓库**

```bash
# 今天的 git 提交记录
git log --since="today 00:00" --until="tomorrow 00:00" \
  --pretty=format:"%h %s (%an, %ar)" --name-status 2>/dev/null || \
git log --since="midnight" --pretty=format:"%h %s (%an, %ar)" --name-status

# 未提交的变更（含暂存区）
git status --short
git diff --stat
git diff --cached --stat
```

**1b. 关联仓库扫描（跨仓库必做）**

扫描父目录下所有 git 仓库，找出今天有修改的：

```bash
# 找出同层/父层目录下所有 git 仓库，逐一检查今天的提交
PARENT=$(git rev-parse --show-toplevel 2>/dev/null | xargs dirname)
for repo in $(find "$PARENT" -maxdepth 3 -name ".git" -type d 2>/dev/null | xargs -I{} dirname {}); do
  COMMITS=$(git -C "$repo" log --since="today 00:00" --oneline 2>/dev/null)
  DIRTY=$(git -C "$repo" status --short 2>/dev/null)
  if [ -n "$COMMITS" ] || [ -n "$DIRTY" ]; then
    echo "=== $repo ==="
    echo "$COMMITS"
    echo "$DIRTY"
  fi
done

# 今天修改过的源码文件（跨目录，按后缀过滤）
TODAY=$(date +%Y-%m-%d)
find "$PARENT" -maxdepth 5 \( -name "*.swift" -o -name "*.rs" -o -name "*.py" \
  -o -name "*.go" -o -name "*.ts" -o -name "*.sql" \) \
  -newer "$PARENT" -not -path "*/.git/*" 2>/dev/null \
  | xargs ls -lt 2>/dev/null | grep "$(date +'%b %e\|%b  %e')" | head -40
```

**1c. Skill / 计划文件变更**

```bash
# 今天新建或修改的 skill 文件
find ~/.claude/skills -name "SKILL.md" -newer ~/.claude/skills -type f 2>/dev/null | head -20

# 今天修改的计划文件
find ~/.claude/plans -name "*.md" -newer ~/.claude/plans -type f 2>/dev/null | head -10
```

### Step 2 — 读取任务与上下文

按优先级依次检查：
1. **当前对话中的 TodoWrite 任务列表**（最优先，每条 todo 对应一个任务）
2. `~/.claude/plans/*.md` 中最近修改的计划文件（补充背景）
3. `docs/daily/` 下昨天的日报（了解延续任务）
4. 当前对话内容（补充 git 无法体现的决策与细节）
5. 当天已有 `docs/daily/<YYYY-MM-DD>.md`（增量更新时必须读取，避免重复或遗漏）

扫描对话时，**主动提取以下信号**：
- 提到了哪些文件路径（尤其是非当前仓库的路径）
- 提到了哪些技术栈、服务名、数据库表名
- 是否有「前后端联动」的描述（前端改字段 → 后端同步 → 数据库迁移）
- 是否有「顺手修了 X」「同时调整了 Y」等附带工作

### Step 2.5 — 遗漏扫描（生成前必做）

在整理任务列表前，逐项自检：

| 检查项 | 问题 |
|--------|------|
| **后端 / 服务端** | 今天是否改过后端代码、接口、数据库迁移文件？ |
| **跨仓库联动** | 前端改了字段，后端有没有对应修改？两边都要记录 |
| **基础设施 / 脚本** | Docker、CI、部署脚本、环境配置有没有动过？ |
| **工具与 Skill** | 有没有新建或修改 Claude skill / 计划文件 / rules？ |
| **配置与常量** | 有没有改过 feature flag、额度、阈值等业务配置？ |
| **调试过程** | 有没有花了较长时间排查但最终未提交的探索过程？ |
| **文档 / 规则** | 有没有更新 AGENTS、CLAUDE、README、PRD、技术方案、日报、记忆文档？ |
| **用户决策** | 用户是否推翻了旧规则、明确了新的默认行为或验收标准？ |
| **验证结果** | 构建、测试、脚本、手动验证是否通过；失败或未执行也要记录原因。 |

**若发现遗漏**：立即补充采集（回到 Step 1b），再继续生成。

**重要：** 生成前至少做一次“任务清单 vs git diff/status vs 对话关键事件”的交叉核对，确保日报覆盖所有重要工作，而不是只覆盖最后一次修改。

### Step 3 — 以任务为单位结构化

**核心原则：每个任务独立成节，按以下四个维度展开。**

| 维度 | 说明 |
|------|------|
| **做了什么** | 任务目标与最终结果，一句话说清 what + why |
| **完整流程** | 从发现问题/接到需求，到完成的完整步骤，体现思路推进过程 |
| **遇到的问题 & 解决** | 三段式：现象 → 根因 → 解决方向（不写实现代码） |
| **经验沉淀** | 这件事让你学到了什么？下次遇到同类问题怎么处理？ |

**同时识别「可固化为 Skill」的流程：**

在整理每个任务时，扫描是否存在满足以下任一条件的操作流程：
- 今天重复执行了 2 次以上的操作
- 步骤固定、可复用，下次遇到同类场景仍需要执行
- 需要记住特定配置、ID、命令序列才能完成
- 解决了一个「以前不知道怎么做、现在弄清楚了」的问题

满足以上条件的，记入 `## 💡 待沉淀为 Skill` 章节，提出建议。

### Step 3.5 — 生成 Agent 快速读取摘要

在写入正文前，必须先生成一个短摘要区，放在 Markdown 文件最前部的元信息之后、任务正文之前。

**设计目标：**
- 使用渐进式披露思想，让 Agent / LLM 先用极少 Token 理解当天主线。
- 摘要区只保留跨任务概览、关键结论、风险与后续动作；不要复述完整流程。
- 后续 Agent 若只需要判断“今天做过什么、有哪些经验可复用”，应优先读取摘要区；需要细节时再展开任务正文。

**摘要区必须包含：**

| 字段 | 内容要求 |
|------|---------|
| **今日主线** | 1 句话概括当天最重要的工作方向。 |
| **任务索引** | 用短列表列出任务编号与任务名，便于跳转正文。 |
| **关键结果** | 2-4 条结果性结论，只写 outcome。 |
| **重要问题** | 0-3 条当天最值得记住的问题或风险。 |
| **可复用经验** | 1-3 条可迁移到后续任务的判断依据或流程经验。 |
| **后续动作** | 0-3 条真实待办；没有则写“暂无”。 |

**摘要区约束：**
- 总长度控制在 120-250 中文字左右；长周期任务较多时最多不超过 400 中文字。
- 不粘贴代码，不列完整文件清单，不展开命令输出。
- 每条内容应能帮助后续 Agent 判断是否需要继续读取正文。
- 如果是增量更新已有日报，必须同步更新摘要区，确保它覆盖当天所有已记录任务。

### Step 3.6 — 工时草拟与用户确认（task_hours 块）

> ⚠️ **强制确认环节**。task_hours 是任务↔日报关联的唯一 source of truth；agent 单方面推断错误会直接污染 ROI 仪表盘和 `npm run daily:backlinks` 派生的双链。**交互式触发必须等用户裁决**；非交互触发须在日报里标 `task_hours_confirmed: false`。

#### 3.6.1 扫当前 sprint 的活跃任务清单

读 `state/program-state.yaml` 的 `current_sprint`（如 `SP10`），然后：

```bash
SPRINT=$(grep '^current_sprint:' state/program-state.yaml | awk '{print $2}')
PAL_TASKS_DIR="$PAL_BASE_PATH/../1-规划/3-任务/$SPRINT"

# 列出所有任务卡，过滤已完成 / killed
for f in "$PAL_TASKS_DIR"/*.md; do
  # 读 frontmatter.状态（Notion 同步字段）
  STATUS=$(awk '/^---$/{c++; next} c==1 && /^状态:/{print $2; exit}' "$f")
  case "$STATUS" in
    "已完成"|"killed"|"cancelled") continue ;;
  esac
  SLUG=$(basename "$f" .md)
  # 读问题描述作为人类可读 title
  TITLE=$(awk '/^---$/{c++; next} c>=2{print; exit}' "$f")
  echo "$SPRINT/$SLUG | $TITLE"
done
```

非主机设备走 SSH：`ssh "$PAL_SSH_HOST" "ls /Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop/PAL-Obsidian/1-规划/3-任务/$SPRINT/*.md"` 然后逐个 `cat` 解析（或写一个 helper 一次性返回 JSON）。

#### 3.6.2 从 Toggl Track API v9 读取今日记录

按 `references/toggl-track-notion-sync.md` 执行：

```bash
python3 plugins/pal-core/skills/daily-report/toggl_track.py \
  --date "$TODAY" --timezone Asia/Shanghai
```

硬性规则：

- API Token 只能来自 `TOGGL_TRACK_API_TOKEN`、兼容名 `TOGGL_API_TOKEN`、
  已被 Git 忽略的 `.env`，或 macOS Keychain
  `pal-daily-report-toggl-track`
- Token 不得进入 config、日报、Git、聊天或输出
- 只能通过 `toggl_track.py` 发起认证请求，禁止在 shell 中拼接凭据
- 将 entry 的 description / project / tags 与 3.6.1 活跃任务做候选匹配
- 运行中 entry 标为临时值，不能绕过用户确认
- Toggl 记录是工时证据，不是任务归属的最终裁决

成功时设置 `task_hours_source: toggl_track`。Token 缺失、认证失败或网络不可达
时不阻断日报，进入 3.6.3 推算并设置 `task_hours_source: inferred`。

#### 3.6.3 agent 补充推算草案

以 Toggl 记录为总时长基线，结合对话历史、TodoWrite 任务列表、git log 时间戳
补充任务归属；若 Toggl 不可用，则沿用原推算逻辑。浮点小时保留 0.5h 精度，
尽量只分配给步骤 3.6.1 的活跃任务。Key 使用标准 task slug：
`SP##/<slug>`。

#### 3.6.4 强制向用户确认（交互式触发）

把草案 + 候选清单展示给用户：

```
今日 task_hours 草案（请确认或修正）：

✏ 推算分配：
  [1] SP10/task-roi-mvp-a  · 完成 PAL 基于任务的ROI测算功能 - MVP  · 8.0h

📋 当前 SP10 其他活跃任务（你今天有动其中的吗？）：
  [2] SP10/lumos-v1-4-0-功能开发-ai回复卡
  [3] SP10/lumos-v1-4-0-功能开发-语音输入卡
  [4] SP10/lumos-v1-4-0-功能开发-其他
  [5] SP10/lumos-v1-4-0-发布-运营
  [6] SP10/ai架构-里程碑-2-优化
  [7] SP10/个人账号运营-vlog视频

操作：
  • 直接 enter / Y → 采用推算
  • "1=10, 3=2"   → 改 [1] 为 10h，新增 [3]=2h
  • "drop 1"      → 删 [1]
  • "ghost: SP10/new-slug=4" → 手动加 Notion 暂无的任务（会触发 ghost 警告但允许写入）
  • "skip"        → 当日纯杂项无任务归属，task_hours 写空 map {}
```

裁决规则：
- **未收到用户回复前不允许进入 Step 4**（防止 agent 自言自语污染数据）
- 任何"ghost: <slug>=<h>"形式写入的 task slug 会在下次 `roi:refresh` 触发 ghost 警告，提醒用户去 Notion 建对应任务卡
- frontmatter 加 `task_hours_confirmed: true`
- frontmatter 加 `task_hours_source: toggl_track | manual | inferred`
- 只有确认后才允许执行 Step 6.5 Notion 工时同步

#### 3.6.5 非交互触发的降级路径

`Stop` hook / 80% 阈值自动触发场景：
- 走步骤 3.6.2/3.6.3 取数或推算后直接落地
- frontmatter 加 `task_hours_confirmed: false`
- frontmatter 加 `notion_hours_synced: false`
- 在日报正文 `## Agent 快速读取摘要` 之前插入 callout：
  ```
  > [!warning] task_hours 未经人工确认
  > 本份日报由自动触发生成，task_hours 是 agent 的估算。下次手动调起 daily-report 会被提示回看确认。
  ```
- 下次任何 daily-report 会话开头先扫 `8-日报/<user>/` 找 `task_hours_confirmed: false` 的日报，列给用户补确认


### Step 4 — 生成 Markdown

模板说明：

- **沉淀段（v5.1 新增）**：由 Step 5.6 自动填充。如果当次 session 没有调用 upsert（例如 Ollama 不可用 / 用户跳过），此段写"本次未沉淀（原因：...）"。
- **frontmatter（v2 ROI MVP 新增）**：每份新日报必须以 YAML frontmatter 开头（见下方模板）。增量更新规则见本节末"Frontmatter 协议"段。

**严格遵循以下模板：**

```markdown
---
user: {user_id}
date: {date}
theme: {theme}
task_hours:
  {task_slug_1}: {hours_1}
  {task_slug_2}: {hours_2}
task_hours_source: {toggl_track|manual|inferred}
task_hours_confirmed: {true|false}
notion_hours_synced: {true|false}
---

# 日报 · YYYY-MM-DD · <主题>

> 主题：10 字以内概括当天最核心的工作方向（如「引导页流程重构」「AI 留言性能优化」「订阅体系接入」）
> 项目：<项目名>  ·  分支：<当前分支>  ·  用时：~<估算小时>h

## Agent 快速读取摘要

> 渐进式披露入口：先读本区了解当天主线；需要细节时再跳到对应任务正文。

- **今日主线：** 1 句话说明今天围绕什么目标推进。
- **任务索引：**
  - 任务 1：<任务名称>
  - 任务 2：<任务名称>
- **关键结果：**
  - 结果 1
  - 结果 2
- **重要问题：**
  - 问题或风险 1（没有则写“暂无”）
- **可复用经验：**
  - 经验 1
- **后续动作：**
  - 待办 1（没有则写“暂无”）

---

## 任务 1：<任务名称>

**做了什么：** 一句话概述目标与结果

**完整流程：**
1. （触发点）为什么要做这个任务
2. （排查/设计）怎么分析问题或规划方案
3. （执行）按什么顺序推进
4. （验证）如何确认结果符合预期

**遇到的问题：**

> 问题 1：<简短标题>
- 现象：...
- 根因：...
- 解决：...

> 问题 2：...（无问题则省略此块）

**经验沉淀：**
- 下次遇到类似情况，应该先...
- 这类问题的根源通常是...
- 值得记住的判断依据：...

---

## 任务 2：<任务名称>

（同上结构）

---

## 🛠 新建 / 更新的 Skill

| Skill 名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| `skill-name` | ... | `~/.claude/skills/xxx/SKILL.md` |

> 当日无 skill 变更则省略此章节。

## 💡 待沉淀为 Skill

| 建议 Skill 名称 | 触发场景 | 沉淀理由 |
|--------------|---------|---------|
| `skill-name` | 遇到 X 类问题时触发 | 步骤固定可复用 / 今天重复操作 / 需要记住特定配置 |

> 当日无 skill 机会则省略此章节。

## 📋 明日待办

- [ ] 优先级高：...
- [ ] 优先级中：...

---

## 沉淀

> 本次会话沉淀到 PAL 9-memory：
> - 写入实体：<entities>
> - 写入关系：<edges>
> - 关联任务：<task wikilinks>
>
> 由 `pal-memory.upsert` 触发；详见 audit log `system/audit/memory.write.jsonl`。

---

*自动生成 by daily-report skill · <timestamp>*
```

---

**Frontmatter 协议（v2 ROI MVP）**：

- 必填字段：`user / date / theme`
- ROI 必填：`task_hours: { "SP##/<slug>": <浮点小时> }`（key 必须是标准 task slug 形式，与 `pal-cli memory write --task` 接受的三种形式一致）
- 多任务时 `task_hours` 为 YAML map；当日纯杂项无任务归属时 map 可为空 `task_hours: {}`，但 frontmatter 块本身必填
- 双链派生必填：`task_hours_confirmed: true | false`（交互式触发 + 用户确认 → true；非交互兜底 → false）
- 工时来源必填：`task_hours_source: toggl_track | manual | inferred`
- Notion 状态必填：`notion_hours_synced: true | false`；只有写后复查成功才为 true
- **增量更新规则**：
  - 若现有日报**无 frontmatter**（如 2026-06-22 之前历史日报，以 `# 日报` 开头）→ 在第 1 行 `# 日报` 之前插入完整 frontmatter 块
  - 若已有 frontmatter → **只 merge `task_hours` 子键**（累加小时数，不覆盖现有 `user / date / theme`；同一 task slug 的值取两次之和）
  - 增量更新逻辑在 Step 5a 写本地文件**之前**执行，确保本地版与 PAL 主机版 frontmatter 一致

### Step 5 — 主题决定 + 文件命名

文件名格式：`<YYYY-MM-DD>-<主题 slug>.md`

- **当日首次写**：agent 根据今日主线生成 ≤ 10 中文字主题
- **当日增量**：
  ```python
  from helpers import find_existing_report_for_date
  existing = find_existing_report_for_date(daily_dir, today)
  ```
  若命中则**沿用原文件名**（主题保持稳定，避免重命名抖动）。
- **当日主题已演变**：当 agent 认为主题应改：
  - 询问用户「今日主题已从 `<旧>` 演变为 `<新>`，是否重命名？」
  - 用户确认后 `git mv` 两边的文件（本地 + 主机端，通过 pal-cli 手动操作）
- **当日多线**：agent 一天做了完全不同的事，多份 `<date>-*.md` 共存；摘要区写"今日多线"
- **slug 生成**：通过 `helpers.slugify_theme()`，规则同 `pal-cli report append --theme`

### Step 5a — 写入本地项目

用 Write 工具写到 `<current-project>/docs/daily/<date>-<theme>.md`（目录不存在时先创建）。

**增量写入要求：**
- 若当天日报已存在，先读取原文，更新摘要区 + 相关任务节，不要覆盖
- 新任务追加为 `## 任务 N`；同任务后续修正合并到原任务节
- 写入后复查：任务编号 / 摘要区 / 明日待办 / 沉淀段 一致

> ⚠️ **Step 5a 仅限写当前项目的 `docs/daily/` 目录**（与 PAL-Obsidian 无关）。无论在哪台设备都应执行此步骤。
>
> **Step 5a ≠ PAL-Obsidian 写入**。以下操作对非 Mac mini 设备**严格禁止**：
> - `cp`/`mv`/`Write` 到 `pal_local_path`（即任何 `PAL-Obsidian/8-日报/…` 路径）
> - 把日报额外复制一份到本机 PAL-Obsidian 目录
>
> 非 Mac mini 设备（`IS_PAL_HOST == false`）执行完 Step 5a 后，直接跳到 **Step 5b（SSH 强制同步）**，不做任何本地 PAL-Obsidian 写入。

### Step 5b — 通过 `pal-cli report append` 同步到 PAL 主机

> **v2 ROI 协议**：从 stdin pipe 给 `pal-cli report append` 的内容必须以完整 frontmatter（含 `task_hours`）开头（即 `---\n...\n---\n` 块）。如果该 CLI 当前会清洗 frontmatter，先调 `pal-cli report append --version` 确认，或在 SKILL 中标 TODO 给 pal-cli 提 patch。本 Task 仅改 daily-report skill；CLI 侧如需改造请单独提 ticket。

**设备分支（必读）：**

| 设备 | IS_PAL_HOST | Step 5b 行为 |
|------|-------------|------------|
| Mac mini（`macmini`） | ✅ true | 可选：直接调本机 `pal-cli`，或 SSH 自环 |
| MacBook（`mbp`）或其他 | ❌ false | **必须**：通过 SSH 同步到 Mac mini，**禁止**回退到本机写 |

MacBook 上的**强制 SSH 同步**方式（Bash，推荐）—— 使用 Step 0f 探活得到的 `$PAL_SSH_HOST`：

```bash
PAL_CLI="/Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop/agent-harness/.venv/bin/pal-cli"
cat "docs/daily/${date}-${slug}.md" | \
  ssh "$PAL_SSH_HOST" "PATH=/opt/homebrew/bin:\$PATH $PAL_CLI report append \
    --date ${date} \
    --theme ${slug} \
    --user ${user_id} \
    --content-file - \
    --mode replace"
```

> **重要**：`$PAL_SSH_HOST` 由 Step 0f 探活时按 `palhost-lan → palhost-ts` 顺序选定，已经过验证可用。这里**不要**硬编码 `palhost-lan`，否则在出差等异网场景下会持续失败。

**失败时**（必须满足：`$PAL_SSH_HOST` 为空 **或** SSH 命令在已知可达通道上仍报错）：

```bash
# 先确认是不是因为 0f 没探活到任何通道
if [ -z "$PAL_SSH_HOST" ]; then
    # 真正两条通道都不通 → 走 pending
    printf '\n\n<!-- pal-sync: pending; reason: ssh unreachable (lan+ts both failed) -->\n' \
        >> "docs/daily/${date}-${slug}.md"
    echo "⚠ PAL 主机不可达（LAN + Tailscale 都失败）：本地草稿已加 pal-sync: pending 标记"
else
    # PAL_SSH_HOST 有值但同步失败 → 临时网络抖动，重试一次再加 pending
    echo "⚠ 经 $PAL_SSH_HOST 同步失败，等待 5s 后重试..."
    sleep 5
    # ... 重试同步命令；仍失败再加 pending 标记
fi

# ⛔ 任何情况下都不允许 cp/Write 到本机 PAL-Obsidian 作为 fallback
```

**自动 fallback 流程要点**：
1. 探活阶段（Step 0f）已经做了 LAN → Tailscale 的通道选择
2. 同步阶段（本节）只用探活通过的通道
3. **不要在同步阶段再次硬编码 `palhost-lan`**——这是历史 bug 高发区
4. 只有两条通道都不通才走 pending；不要因为一条通道超时就直接放弃远端传输

**关键说明**：
- **IS_PAL_HOST == false 时，Step 5b 是唯一合法的 PAL 写入路径**；失败时不得用本机 PAL-Obsidian 目录兜底
- **--mode replace**：传完整内容，让主机端按内容覆盖文件（避免本地+主机各自做合并造成的不一致）
- 主机端会自动 `git add -A && git commit` 并按 10 分钟节流 `git push`

> ⚠️ **Step 5b 成功 ≠ PAL 同步完成。**
> pal-cli report append 只完成了"文件写入 + git commit"，**INDEX.md 不会自动更新**。
> 必须继续执行 **Step 5d**，否则日报不会出现在 Sprint 矩阵索引中。

### Step 5c — 失败恢复：补传 pending 草稿

如果本地文件末尾有 `<!-- pal-sync: pending -->` 标记，每次 daily-report 启动时优先尝试补传：

```python
import re

content = open(local_path).read()
if "<!-- pal-sync: pending" in content:
    # 去掉 marker，重传
    cleaned = re.sub(r"\n+<!-- pal-sync: pending[^>]*-->\n*$", "\n", content)
    try:
        pal_call("report", "append",
                 "--date", date, "--theme", slug, "--user", user_id,
                 "--content-file", "-", "--mode", "replace",
                 stdin=cleaned)
        # 成功 → 本地也清理 marker
        with open(local_path, "w") as f:
            f.write(cleaned)
        print("✓ pal-sync pending 补传成功")
    except PalError:
        pass  # 继续保持 pending
```

### Step 5d — 更新日报索引（INDEX.md）

> ⚠️ **这是独立步骤，不是 Step 5b 的附带效果。** pal-cli 不触发 index 更新，必须单独执行。

**MacBook（IS_PAL_HOST == false）** — 通过 Step 0f 探活的 `$PAL_SSH_HOST` 通道执行：

```bash
ssh "$PAL_SSH_HOST" "cd /Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop && \
  PATH=/opt/homebrew/bin:\$PATH \
  node scripts/daily-index-rebuild.mjs --upsert <user_id> <filename> --non-interactive"
```

注意：
- **不要硬编码 `palhost-lan`**——使用 Step 0f 探活得到的 `$PAL_SSH_HOST`（可能是 `palhost-lan` 或 `palhost-ts`）
- 必须 `cd` 到 PAL 根目录，脚本用相对路径引用其他文件
- 必须显式带 `PATH=/opt/homebrew/bin:$PATH`，SSH 登录不加载 homebrew 路径
- `<filename>` 是 pal-cli 返回的 `remote_path` 中的文件名部分（如 `2026-05-20-v120_ai测试方案.md`）

**Mac mini（IS_PAL_HOST == true）** — 本机直接执行：

```bash
cd /Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop && \
  node scripts/daily-index-rebuild.mjs --upsert <user_id> <filename> --non-interactive
```

**判定路径：**
- 退出码 0，输出 `✓ ... (N entries)` → 完成，继续 Step 5.6
- 非 0（异常）→ 自动 fallback 全量重建（仍使用 `$PAL_SSH_HOST`）：
  ```bash
  ssh "$PAL_SSH_HOST" "cd /Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop && \
    PATH=/opt/homebrew/bin:\$PATH node scripts/daily-index-rebuild.mjs --non-interactive"
  ```
- fallback 仍失败 → 写 warning 到日报末尾 `<!-- daily-index: failed; run npm run daily:index 手动修复 -->`，**不阻断**整个日报生成流程

**为什么 `--non-interactive`：** skill 自动触发时无法处理人类裁决；不规范文件名会被静默纳入 + 待办清单写到 `tmp/daily-rename-suggestions-<date>.txt`，等用户下次手工跑 `npm run daily:index` 时确认。

**INDEX.md 现已采用 Sprint 矩阵布局**（2026-05-18 起）：按 Sprint 分组，每个 Sprint 渲染一个 14 天 日期 × 用户 矩阵。Sprint 由日报日期自动归属。

---

### ✅ PAL 同步完成核销清单

Step 5b + 5d 执行后，**必须逐项确认**，两条都满足才算同步完成：

- [ ] **Step 5b**：`pal-cli report append` 返回了 `git_commit` 字段（有 commit hash）
- [ ] **Step 5d**：`daily-index-rebuild.mjs` 输出 `✓ INDEX.md (N entries)`，且 N ≥ 上次执行时的数量

**任何一条未满足 → 不得停手，继续排查或补跑对应步骤。**

---

### Step 6 — 触发 task-roi 派生 + 任务卡日报回链（ROI 接入）

日报与索引都写完后，**串行**运行以下两个命令以再生 ROI 仪表板 + 任务卡末尾的日报回链段：

```bash
cd <pal-root> && npm run roi:refresh && npm run daily:backlinks
```

> ⚠️ 顺序不能颠倒：`daily:backlinks` 也依赖 `task_hours` source of truth，但它的输出（任务卡末尾 `<!-- daily-backlinks:start --> ... <!-- daily-backlinks:end -->` 块）独立于 ROI 仪表板，两者无数据依赖，串行只是为了便于读 stderr 调试。

**预期行为：**

该命令由 `scripts/derive-task-roi.mjs` 驱动，执行以下操作：
1. 扫描 `3-任务/SP##/` 下所有任务卡的 frontmatter
2. 聚合 `PAL-Obsidian/8-日报/` 下所有日报的 `task_hours` 块
3. 按任务维度合并任务描述 + 工时数据 + 完成度
4. 输出三份派生物：

   - **`PAL-Obsidian/9-记忆/_index/task-roi.jsonl`** — 机器可读聚合数据（每行一个 task record）
   - **`PAL-Obsidian/0-运行时/任务ROI.md`** — Markdown 仪表板（可在 Obsidian / GitHub 直读）
   - **`PAL-Obsidian/0-运行时/任务ROI.html`** — 交互式 HTML 仪表板（可在浏览器打开）

**预期输出示例：**

```
[ROI] tasks=18 dailies=42 enriched=18
[ROI] skipped: non-sp-dirs=2 no-frontmatter-dailies=3
[ROI] ghost hours (referencing unknown tasks): 0
[ROI] wrote PAL-Obsidian/9-记忆/_index/task-roi.jsonl
[ROI] wrote PAL-Obsidian/0-运行时/任务ROI.md
[ROI] wrote PAL-Obsidian/0-运行时/任务ROI.html
```

**失败处理：**

stderr 中可能出现以下 warn（**只提示不阻断**）：
- `[warn] ghost task <slug>` — 任务卡在 PAL-Obsidian/9-memory 中无对应 entity（悬空引用）
- `[warn] unknown owner <user_id>` — 日报归属的用户 ID 不在 Notion owner list 中
- `[warn] outcome incomplete <task>` — 任务的 `outcome` 字段未填或为空

若退出码非 0（致命错误，如脚本运行时异常）：
- 告知用户"task-roi 派生失败，但日报已写入；详见 stderr 诊断信息"
- 这**不阻断**整个日报工作流；日报仍应正常生成并推送
- 用户可稍后手工运行 `npm run roi:refresh` 修复

**关键说明：**

- **Step 6 在 Step 5d 成功后自动触发**，无需用户干预
- Markdown + HTML 派生物作为**开放式仪表板**：所有相关人员（PM / Hermes / Claude / Codex）均可读，但 **source of truth 是 task-roi.jsonl**（用于后续自动化处理）
- derive-task-roi.mjs 支持手工运行：`npm run roi:refresh` 或 `npm run roi:test`（详见 Task 4.2 文档）
- `daily:backlinks` 把日报 frontmatter.task_hours 反向倒排到任务卡末尾的 `<!-- daily-backlinks:start --> ... <!-- daily-backlinks:end -->` 标记块。Notion pull 不会动该块（pull 只动 frontmatter 和 `> Last edited` 之前的正文）；想解除某个日报↔任务关联，请改对应日报 task_hours，再跑 `npm run daily:backlinks`。

---

### Step 6.5 — 幂等同步累计工时到 Notion 任务池

仅当 `task_hours_confirmed: true` 时执行。完整协议见
`references/toggl-track-notion-sync.md`。

1. 使用已连接的 Notion 工具 fetch 私有配置中的 `notion_database_id`，
   每次确认标题字段仍为 `notion_title_property`、数字字段仍为
   `notion_hours_property`；不得依赖公开 Skill 中的硬编码数据库 ID。
2. 对每个 task slug 聚合所有日报中 `task_hours_confirmed: true` 的工时。
3. 优先读取任务卡 frontmatter 的 `notion_page_id`；否则以
   `问题描述 + 任务阶段` 做唯一匹配。零条或多条时禁止写入。
4. 将重算得到的累计值直接设置到 `工时(h)`，禁止
   `Notion 当前值 + 今日工时`。
5. 再次 fetch page 验证；一致后把日报 `notion_hours_synced` 改为 `true`。

Notion 不可用或匹配不唯一时，日报与 ROI 流程继续，但保留
`notion_hours_synced: false`，并在结果中明确列出待同步 task slug。

---

### Step 5.6 — 内嵌 pal-memory upsert（按 PS 切片沉淀）

收尾时把本次 session 按 problem-space 切片，对每个 PS 调一次 `pal-memory.upsert`。
结果摘要写回日报的 `## 沉淀` 段。

> ⚠️ **执行模式说明（必读，防止误判跳过）**
>
> 以下伪代码中 `from pal_client import pal_call` 是**概念说明**，不是要求 agent 在本机运行 Python。
> **无论 agent 在 MacBook 还是 Mac mini，均应执行本步骤**，具体路径如下：
>
> | 条件 | 执行方式 |
> |---|---|
> | Mac mini 本机运行 | 直接调 `pal-cli memory write ...` |
> | MacBook（无本地 pal-cli）| 用 Bash 通过 SSH 调：`echo '<triples>' \| ssh "$PAL_SSH_HOST" "PATH=/opt/homebrew/bin:\$PATH <pal-cli> memory write --triples-file -"`。`$PAL_SSH_HOST` 由 Step 0f 探活得到（按 `palhost-lan → palhost-ts` 顺序选用第一个通的） |
> | `PAL_SSH_HOST` 未设 | **必须先跑 Step 0f 探活**填充该变量；如果探活后仍为空，说明 LAN + Tailscale 都不通，本步骤跳过并在沉淀段写明原因 |
> | Mac mini 无本地 Ollama | **不影响**。embedding 在 Mac mini 服务端完成（Mac mini 自带 Ollama） |
>
> **"MacBook 无本地 pal-cli 虚拟环境"不是跳过的合法理由。** agent 应构造 SSH 命令直接调用 Mac mini 上的 pal-cli，与 `palr` helper 方式完全一致。

**upsert 两阶段速查**（完整说明见 `pal-memory` skill §2）：

```
前置：确认 $PAL_SSH_HOST 已由 Step 0f 探活填充（palhost-lan 或 palhost-ts）

阶段 A — Claude 自己推理（无外部依赖）
  1. SSH 拉 extraction prompt：ssh "$PAL_SSH_HOST" "pal-cli skills get entity-extraction"
  2. SSH 拉 ontology：ssh "$PAL_SSH_HOST" "pal-cli ontology dump"
  3. Claude 读 session 内容 → 输出 JSONL triples
     格式：{"subject":"slug-a","predicate":"relation","object":"slug-b","reasoning":"..."}

阶段 B — SSH pipe 到 Mac mini（由 pal-cli 完成落盘+embedding）
  printf '<triples>' | ssh "$PAL_SSH_HOST" "PATH=/opt/homebrew/bin:$PATH <pal-cli> \
    memory write --triples-file - --task <slug> --problem-space <ps-slug>"

⚠️ embedding 在 Mac mini Ollama 服务端发生，agent 不感知
⚠️ MacBook 无本地 pal-cli ≠ 跳过理由；直接构造 SSH 命令即可
⚠️ 禁止硬编码 palhost-lan；必须用 $PAL_SSH_HOST，否则跨网络场景会持续失败
```

**步骤**：

1. **识别 PS**：从对话/任务中提取每条工作的 problem_space slug。判断依据：
   - 用户/任务里出现的 task slug 关联的 PS
   - 主题词 + 实体集与上一段无交集 → 换了 PS
   - 用户明说"换个话题"
   - 默认 `None`（"unassigned"，无明确 PS）

2. **切片**：

   ```python
   from helpers import split_session_by_problem_space

   session_entries = [
       {"problem_space": "ps-emotion-entry", "task_excerpt": "..."},
       {"problem_space": "ps-emotion-entry", "task_excerpt": "..."},
       {"problem_space": "ps-ai-trigger",   "task_excerpt": "..."},
   ]
   segments = split_session_by_problem_space(session_entries)
   ```

3. **每个 PS upsert 一次**（agent 端跑抽取，主机端只校验+落盘）：

   ```python
   # IMPORTANT: This is GUIDANCE pseudocode for the agent's LLM.
   # `my_llm_extract(prompt, ontology, excerpt)` represents the agent calling its OWN LLM
   # to perform extraction in the conversation context — there is NO actual Python
   # function named `my_llm_extract`. The agent should literally run the prompt against
   # its model and parse the resulting JSONL.
   # `current_task_slug` should be set by the agent to the active task slug for the day
   # (typically the same task passed into the daily-report invocation).
   current_task_slug = "<today's task slug from caller / daily context>"
   import json, sys
   sys.path.insert(0, "<pal-repo>/skills/pal-memory")
   from pal_client import pal_call, PalError
   from ontology_cache import get_ontology, get_extraction_prompt

   upsert_summary = []
   for seg in segments:
       ps = seg["problem_space"]
       excerpt = seg["task_excerpt"]

       # ① 拉 ontology + prompt（缓存）
       ontology = get_ontology()
       prompt = get_extraction_prompt()

       # ② agent 自己的 LLM 在本上下文执行抽取（见 pal-memory/extraction_workflow.md）
       triples = my_llm_extract(prompt, ontology, excerpt)

       if not triples:
           upsert_summary.append({"ps": ps, "skipped": "no triples extracted"})
           continue

       # ③ 提交到主机
       jsonl = "\n".join(json.dumps(t, ensure_ascii=False) for t in triples) + "\n"
       try:
           env = pal_call("memory", "write",
                          "--triples-file", "-",
                          "--task", current_task_slug,
                          *(["--problem-space", ps] if ps else []),
                          stdin=jsonl)
           data = env["data"]
           upsert_summary.append({
               "ps": ps or "(unassigned)",
               "wrote_entities": [e["slug"] for e in data["wrote_entities"]],
               "wrote_edges": len(data["wrote_edges"]),
               "warnings": data.get("warnings", []),
               "audit_log_id": data["audit_log_id"],
           })
       except PalError as e:
           upsert_summary.append({"ps": ps, "error": str(e)[:200]})
   ```

   **MacBook 上无本地 pal-cli 时的等效 Bash 实现**（优先用此方式，不要跳过）：

   ```bash
   # 前置：$PAL_SSH_HOST 应已由 Step 0f 探活填充（palhost-lan 或 palhost-ts）

   # ① 拉 extraction prompt
   EXTRACTION_PROMPT=$(ssh "$PAL_SSH_HOST" "PATH=/opt/homebrew/bin:\$PATH \
     /Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop/agent-harness/.venv/bin/pal-cli \
     skills get entity-extraction")

   # ② Claude 自身在对话上下文中执行抽取，输出 JSONL triples（每行一个 triple）
   # （这一步是 agent 的 LLM reasoning，不需要 Bash）

   # ③ 把 triples 写入主机（以下为 Bash 中执行的实际命令）
   PAL_CLI="/Users/sollarzoo/Documents/GitHub/Product-Agentic-Loop/agent-harness/.venv/bin/pal-cli"
   printf '%s\n' '<triple1 json>' '<triple2 json>' | \
     ssh "$PAL_SSH_HOST" "PATH=/opt/homebrew/bin:\$PATH $PAL_CLI memory write \
       --triples-file - \
       --task <task-slug> \
       --problem-space <ps-slug>"
   ```

   > 注：所有命令的 `ssh` 主机必须用 `$PAL_SSH_HOST`，不要硬编码 `palhost-lan`。这是跨网络（出差、异网、VPN 切换）场景下能否成功的关键。

4. **回填 ## 沉淀 段**：渲染 `upsert_summary` 为人类可读 markdown 写进 Step 4 模板的 `## 沉淀` 段。

5. **失败处理**：
   - 任何 PS 的 upsert 失败不阻断整个流程
   - `OLLAMA_UNREACHABLE` / `VOCAB_VIOLATION` / `TASK_NOT_CONDENSED` → 按 pal-memory skill §"失败回退矩阵" 处理
   - 全部失败 → 沉淀段写"本次未沉淀（原因：...）"，日报仍正常生成

6. **顺序约束**：Step 5.6 在 Step 5a (本地写) 之后、Step 5b (PAL 写) 之前 — 沉淀段内容会同时进入本地草稿和 PAL 主机版本。

**调用频率护栏**（来自 pal-memory skill）：每 session × 每 PS 最多 1 次 upsert；单 session PS 切换超过 3 个 → 提示用户拆分 session。

---

## 输出规则

1. **先展示** 日报全文（对话中）
2. **生成 ## 沉淀 段**（Step 5.6 调 pal-memory upsert，按 PS 切片）
3. **写本地项目文件**（`<current-project>/docs/daily/<date>-<theme>.md`）— 所有设备均执行
4. **同步 PAL 主机**（强制 SSH，见下表）

   | 设备 | 操作 |
   |------|------|
   | Mac mini（`device_id == "macmini"`） | 本机 `pal-cli report append` 直接写 |
   | MacBook 或其他（`IS_PAL_HOST == false`）| **必须** SSH 同步到 Mac mini；**禁止**写本机 PAL-Obsidian |

5. **更新索引**（`node scripts/daily-index-rebuild.mjs --upsert <user> <file> --non-interactive`，失败自动 fallback 全量重建；详见 Step 5d）
6. **同步任务累计工时到 Notion**（仅 `task_hours_confirmed: true`；写后复查）
7. 无 git 提交时，基于对话历史生成，标注「无 git 提交」
8. 每次生成或增量更新日报时，**必须**同步更新 `## Agent 快速读取摘要` + `## 沉淀` 段
9. 自动触发时直接执行写入与同步流程，不再向用户请求审批；除非用户明确要求跳过
10. 语言默认中文；用户说「English」则切换
11. **⛔ 非 PAL 主机（`IS_PAL_HOST == false`）严禁**将日报写入或复制到本机 PAL-Obsidian 目录（`pal_local_path`）；SSH 不通时加 `pal-sync: pending` 标记，等待补传，**不得**用本机目录作为 fallback

## 失败恢复矩阵（v5.3）

| 失败 | 行为 |
|---|---|
| **非 PAL 主机写入本机 PAL-Obsidian（任何原因）** | **❌ 严格禁止**。无论 SSH 是否可达，均不得写入本机 `pal_local_path`；SSH 不通时加 `pal-sync: pending`，等待补传 |
| **SSH 不通，IS_PAL_HOST == false** | **必须先按 Step 0f 顺序尝试 `palhost-lan` + `palhost-ts` 两条通道**；只有两条都失败才算真不通。真不通时在项目 `docs/daily/` 文件末尾追加 `<!-- pal-sync: pending; reason: ssh unreachable (lan+ts both failed) -->` 标记；**禁止**用本机 PAL-Obsidian 兜底；下次 daily-report 启动时自动补传（Step 5c）。**禁止**只试 LAN 就声明离线 —— 跨网络场景必然失败 |
| **palhost-lan 超时但未试 palhost-ts** | ❌ 不可接受的判定。Step 0f 探活逻辑必须完整跑完两条通道；不能在第一条超时后直接转 pending |
| **Step 5.6 被跳过（理由为"无本地 pal-cli"）** | **❌ 不合法的跳过理由**。应改用 Bash SSH 命令直接调 Mac mini 上的 pal-cli（见 Step 5.6 §MacBook 无本地 pal-cli 时的等效 Bash 实现） |
| 本地项目写失败（权限/磁盘） | 中止，提示用户检查项目目录权限 |
| ssh 不通 / 主机不可达（IS_PAL_HOST == true） | 本机即是 PAL 主机，pal-cli 直写失败则检查 pal-cli 路径是否正确 |
| 主机端 user 目录不存在 | pal-cli 自动创建 `PAL-Obsidian/8-日报/<user>/`，不阻断 |
| Ollama 不可达（影响 upsert）| 沉淀段写 "本次未沉淀（Ollama unreachable）"，日报仍正常生成 + 推送 |
| VOCAB_VIOLATION | 沉淀段标"被拒绝的 triples"，agent 可在下次会话修正 |
| 部分 PS upsert 成功部分失败 | 已成功的不撤回；失败的列表写进沉淀段 |
| `TASK_NOT_CONDENSED`（来自 pal-memory upsert） | 跳过该 PS 的 upsert；在沉淀段记录"<task> 未凝结，已跳过 PS=<ps>"；其他 PS 继续；日报正常生成 + 推送 |
| Toggl Token 缺失/401/403 | 回退到 agent 推算，标 `task_hours_source: inferred`；不写 Notion，绝不输出 Token |
| Toggl API 网络不可达 | 回退到 agent 推算并向用户说明；日报继续 |
| Toggl 存在运行中 entry | 按当前时间计算临时工时，必须经用户确认后才能同步 |
| Notion 未连接或 schema 变化 | 日报继续，标 `notion_hours_synced: false`，列入 pending |
| Notion 任务匹配为 0 或多条 | 禁止猜测/写入；要求用户选择唯一任务 |
| Notion 写后复查不一致 | 标 `notion_hours_synced: false`，不得报告同步成功 |

---

## 日报质量标准

**以任务为单位，概念优先，不写代码**

- ✅ **完整流程**：从「为什么要做」到「如何验证结果」，体现思路，而不是步骤列表
- ✅ **快速摘要**：文件前部必须有 `## Agent 快速读取摘要`，让后续 Agent 用最少 Token 判断是否需要深入正文
- ✅ **问题描述**：三段式（现象 → 根因 → 解决方向），让未参与的人也能理解
- ✅ **经验沉淀**：写「下次怎么做」，而不是「这次做了什么」——这是最有价值的部分
- ✅ **明日待办**：来自真实 pending 任务，不凭空编造
- ✅ **待沉淀为 Skill**：扫描今日流程，主动识别可复用的操作模式，不等用户提出再记录
- ✅ **重要内容不遗漏**：覆盖代码、文档、配置、调试过程、用户决策、验证结果和跨仓库联动

**禁止：**
- ❌ 粘贴代码、函数名、变量名
- ❌ 列举修改了哪些文件
- ❌ 摘要区复述完整日报，或写成超过正文任务节的长篇总结
- ❌ 只写结论不写过程（「修复了 bug」不够，要写「为什么会有这个 bug，怎么发现的」）
- ❌ 经验沉淀写成操作记录（「我修改了 X 文件」不是经验）
- ❌ 只看当前仓库就生成日报（跨仓库工作必须通过 Step 1b + Step 2.5 主动捞取）
- ❌ 前后端联动改动只记录一侧（两边都要有任务节点，或合并成一个任务写完整调用链）
- ❌ 自动触发时再次询问用户是否同意写入日报，除非用户已明确要求暂停日报

---

## 示例输出

> 文件路径：`docs/daily/2026-04-28-引导页修复.md`

```markdown
# 日报 · 2026-04-28 · 引导页信息提交修复

> 项目：Lumos_Swift  ·  分支：feature/v1.2.0_onborading  ·  用时：~8h

---

## 任务 1：修复个人信息页填写内容未保存的问题

**做了什么：** 排查并修复引导页个人信息（昵称/性别/生日等）填写后不入库的 bug，同时扩展前后端支持全字段提交。

**完整流程：**
1. 用户反馈设置页看不到引导页填写的信息，判断为数据未持久化
2. 沿调用链追查：引导页「下一步」→ 提交逻辑 → 网络请求 → 服务端接收，找到断点
3. 发现前端只发送了账号 ID，其他字段从未包含在请求体中；进一步发现数据库表也缺少对应列
4. 前后端同步扩展：数据库新增字段 → 服务端接口支持接收 → 前端构建完整请求体统一提交
5. 重新走查引导页流程，在设置页验证字段已正确显示

**遇到的问题：**

> 问题 1：提交逻辑中出现自赋值，导致数据未更新
- 现象：字段提交后服务端响应正常，但本地缓存中的值始终是旧的
- 根因：参数名与对象属性同名，赋值时漏写了对象前缀，变成了局部变量自赋值
- 解决：明确区分参数作用域与对象属性，加上显式对象前缀

> 问题 2：性别字段前后端类型不匹配
- 现象：服务端收到的性别值无法识别，写入数据库为默认值 0
- 根因：前端用文字枚举（male/female），后端用数字枚举（1/2），两端约定不一致
- 解决：在前端统一做转换，后端不感知文字枚举，保持接口简洁

**经验沉淀：**
- 遇到「数据提交后不生效」的 bug，优先沿调用链逐层打断点，不要假设某一层没问题
- 前后端字段类型约定要在接口设计时明确，转换逻辑统一放在一侧（通常是前端），避免两边各自处理
- 新增字段时，数据库、接口、前端三层要同步变更，遗漏任何一层都会导致静默失败

---

## 任务 2：将验证码输入改为 6 格独立输入框

**做了什么：** 把邮箱绑定页的单行验证码输入框改造成 6 格独立输入框，提升输入体验与视觉一致性。

**完整流程：**
1. 确认需求：每格显示一个数字，活跃格有光标，已输入格高亮
2. 评估方案：原生多 TextField 管理焦点复杂；选择「单个隐藏输入框 + 自定义格子渲染」方案
3. 实现焦点管理：点击任意格子触发隐藏输入框聚焦，用系统键盘输入
4. 渲染层只负责展示，不处理输入事件，职责清晰
5. 验证：实机测试输入、删除、粘贴验证码各场景

**遇到的问题：**

> 问题 1：粘贴6位验证码时只显示第一个字符
- 现象：从短信复制验证码粘贴后，只有第一格填入了内容
- 根因：输入过滤逻辑截断了超过当前格数的字符，没有考虑批量粘贴场景
- 解决：调整过滤逻辑，允许一次性输入多个字符，再按格数截断分配

**经验沉淀：**
- 自定义输入组件设计时，「隐藏真实输入，自定义渲染」是解耦的好模式，但要提前考虑粘贴等非逐字输入场景
- 输入类组件的测试用例应包含：逐字输入、删除、全选删除、粘贴，缺一容易漏测

---

## 🛠 新建 / 更新的 Skill

| Skill 名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| `daily-report` | 以任务为单位生成日报，沉淀流程经验，双写本地 + PAL 主机 | `~/.claude/skills/daily-report/SKILL.md` |

## 💡 待沉淀为 Skill

| 建议 Skill 名称 | 触发场景 | 沉淀理由 |
|--------------|---------|---------|
| `pal-cli-report-recovery` | 检测到 `<!-- pal-sync: pending -->` 标记时触发 | 自动补传，且能识别多次 pending 的累积修复 |
| `xcode-new-file-checklist` | 在 Xcode filesystem group 中新建 Swift 文件时 | membershipExceptions 注册是 Xcode 16 下的必做步骤，每次新建文件都需要，容易忘记 |

## 📋 明日待办

- [ ] 优先级高：执行数据库迁移并部署服务端新版本
- [ ] 优先级高：为已注册老用户补发 1M 额度
- [ ] 优先级中：模拟器完整走查 onboarding 6 步流程

---

*自动生成 by daily-report skill · 2026-04-28 23:49*
```
