# Daily Report 首次初始化

## 目标状态

初始化完成必须同时满足：

- Agent 能找到 `daily-report/SKILL.md`。
- 私有配置存在且不在 Git 仓库内。
- Toggl Track API 验证成功。
- Notion 任务数据库已连接并确认字段。
- 测试日报可以生成，但未确认的工时不会写入 Notion。

## 1. 安装 Skill

将整个 `daily-report/` 目录复制到 Agent 可发现的 skills 目录。不要只复制
`SKILL.md`；`toggl_track.py`、`helpers.py`、`references/` 和测试都属于
Skill 的一部分。

安装后设置路径，后续命令复用：

```bash
export DAILY_REPORT_SKILL_DIR="/absolute/path/to/daily-report"
test -f "$DAILY_REPORT_SKILL_DIR/SKILL.md"
```

## 2. 创建私有配置

配置查找顺序：

1. 环境变量 `DAILY_REPORT_CONFIG` 指向的文件；
2. `~/.claude/skills/daily-report/config.json`；
3. `<daily-report-skill-dir>/config.json`（旧版兼容，不推荐公开仓库使用）。

推荐做法：

```bash
mkdir -p "$HOME/.claude/skills/daily-report"
cp "$DAILY_REPORT_SKILL_DIR/config.example.json" \
  "$HOME/.claude/skills/daily-report/config.json"
chmod 600 "$HOME/.claude/skills/daily-report/config.json"
```

编辑复制后的文件：

- `device_id`：PAL 主机填 `macmini`；其他机器如 MacBook 填 `mbp`。
- `user_id`：稳定、适合目录名的用户 ID。
- `display_name`：日报显示名。
- `pal_base_path`：`<PAL_ROOT>/PAL-Obsidian/8-日报`。
- `pal_local_path`：`<pal_base_path>/<user_id>`。
- `timezone`：默认 `Asia/Shanghai`。
- `notion_database_id`：Notion 任务数据库 ID。
- `notion_title_property`：任务标题字段，默认 `问题描述`。
- `notion_hours_property`：数字工时字段，默认 `工时(h)`。

禁止把真实 `config.json` 提交到公开 Skill 仓库。

## 3. 获取 Toggl Track API Token

1. 登录 [Toggl Track Profile](https://track.toggl.com/profile)。
2. 滚动到页面底部的 API Token。
3. 复制 Token，但不要发到聊天、Issue、日报或提交记录中。

Toggl Track API v9 使用 HTTP Basic Auth：用户名是个人 API Token，密码是固定
字符串 `api_token`。本 Skill 的 Python 客户端会安全构造认证头，不要手写
`curl -u "$TOKEN:api_token"`。

## 4. 保存 Toggl Token

### 方案 A：项目 `.env`

在执行日报的项目根目录创建 `.env`：

```dotenv
TOGGL_TRACK_API_TOKEN=replace-with-your-token
```

兼容旧变量名 `TOGGL_API_TOKEN`，但新配置统一使用
`TOGGL_TRACK_API_TOKEN`。

立即确认 `.env` 不会进入 Git：

```bash
grep -qxF '.env' .gitignore || printf '\n.env\n' >> .gitignore
git check-ignore -q .env
```

如果 `.env` 曾被跟踪，先旋转 Token，再执行
`git rm --cached .env`，本地文件会保留。

### 方案 B：macOS Keychain（推荐）

使用隐藏输入，避免 Token 出现在 shell history：

```zsh
read -s "TOGGL_TOKEN?Paste Toggl API Token: "
print
security add-generic-password -U \
  -a "$USER" \
  -s "pal-daily-report-toggl-track" \
  -w "$TOGGL_TOKEN"
unset TOGGL_TOKEN
```

客户端读取优先级为：

1. `TOGGL_TRACK_API_TOKEN`
2. `TOGGL_API_TOKEN`
3. 指定或当前目录的 `.env`
4. macOS Keychain

## 5. 验证 Toggl 连接

从项目根目录执行：

```bash
python3 "$DAILY_REPORT_SKILL_DIR/toggl_track.py" \
  --date "$(date +%F)" \
  --timezone "Asia/Shanghai" \
  --dotenv ".env"
```

成功时返回：

```json
{
  "ok": true,
  "date": "YYYY-MM-DD",
  "timezone": "Asia/Shanghai",
  "data": {
    "entry_count": 3,
    "running_count": 1,
    "total_hours": 12.75,
    "entries": []
  }
}
```

真实输出的 `entries` 会包含 description、起止时间和小时数，但绝不包含
Token。出现 `401/403` 时，到 Toggl Profile 重置 Token 后重新保存。

## 6. 连接并验证 Notion

在当前 Agent/客户端中连接 Notion，不要把 Notion Token 写进 Skill 配置。

初始化时执行一次只读检查：

1. fetch `notion_database_id`；
2. 记录返回的 data source ID 到私有配置；
3. 确认 `notion_title_property` 是标题字段；
4. 确认 `notion_hours_property` 是 number 字段；
5. fetch 一个测试任务，确认 Agent 有读权限。

首次真实写入前仍须重新 fetch schema。只有
`task_hours_confirmed: true` 才允许写入工时。

## 7. 运行首次日报

对 Agent 说：

```text
使用 daily-report 生成今天的日报
```

首次运行的预期阶段：

1. 读取并验证私有配置；
2. 读取 Toggl 今日记录；
3. 扫描今日仓库、对话和任务；
4. 展示 task_hours 草案；
5. 等待用户确认；
6. 写本地/PAL 日报与派生数据；
7. 重算累计确认工时并同步 Notion。

未收到用户确认时，流程必须停在第 4 步之后：

```yaml
task_hours_confirmed: false
notion_hours_synced: false
```

## 初始化排错

| 现象 | 检查 |
|---|---|
| 找不到 Skill | 检查完整目录是否位于 Agent 的 skills 搜索路径 |
| 找不到 config | 检查 `DAILY_REPORT_CONFIG` 或默认私有配置路径 |
| 找不到 Toggl Token | 检查变量名、`.env` 路径或 Keychain service |
| Toggl 返回 403 | 重置 API Token，覆盖旧凭据 |
| 今日 0 条记录 | 检查日期、`timezone` 和 Toggl 当日是否有 entry |
| Notion 不可写 | 检查连接权限、数据库 ID、data source 与字段类型 |
| Notion 工时重复 | 禁止累加当前值；从已确认日报重新聚合后覆盖 |
