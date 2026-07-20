# Toggl Track → Daily Report → Notion 工时同步

## 运行时目标

- Toggl Track API：`https://api.track.toggl.com/api/v9`
- Notion 任务池：私有配置的 `notion_database_id`
- Notion data source：私有配置的 `notion_data_source_id` 或 fetch 结果
- 标题字段：私有配置的 `notion_title_property`
- 工时字段：私有配置的 `notion_hours_property`（number）

每次运行仍须 fetch 数据库并确认 schema。初始化步骤见
[getting-started.md](getting-started.md)。

## 凭据

读取优先级：

1. `TOGGL_TRACK_API_TOKEN` 或兼容名 `TOGGL_API_TOKEN`
2. 当前项目、PAL 根目录的 `.env`
3. macOS Keychain service `pal-daily-report-toggl-track`

`.env` 必须被 Git 忽略。禁止把 Token 放进 Skill、日报、Git、聊天或命令
输出。调用 API 必须使用 `toggl_track.py`，禁止在 shell 中拼接认证字符串。

## 取数

```bash
python3 toggl_track.py --date YYYY-MM-DD --timezone Asia/Shanghai
```

实际请求：

`GET /me/time_entries?start_date=<RFC3339>&end_date=<RFC3339>&meta=true`

运行中的 entry 以 `now - start` 计算临时工时并标 `running: true`。

## 任务匹配

匹配优先级：

1. PAL 任务卡 frontmatter 的 `notion_page_id`
2. 标准 task slug 对应的唯一 `问题描述` + `任务阶段`
3. 用户在确认环节明确选择的唯一 Notion 行

零匹配或多匹配不得猜测。Toggl description、project、tag 只用于生成草案；
用户确认后才写 `task_hours_confirmed: true`。

## 幂等同步

Notion 的 `工时(h)` 是该任务的累计确认工时，不是本次增量：

1. 从所有日报聚合 `task_hours_confirmed: true` 的记录。
2. 按 task slug 求和，保留两位小数。
3. fetch 目标 Notion page，复核标题、阶段、page id。
4. 将重算累计值直接设置到 `工时(h)`。
5. 再 fetch 验证写入结果。

禁止执行 `Notion 当前值 + 今日工时`，否则重跑会重复累计。

## 降级策略

| 情况 | 处理 |
|---|---|
| Token 缺失或认证失败 | 回退到推算，标 `task_hours_source: inferred`，不写 Notion |
| Toggl API 不可达 | 同上，并向用户说明 |
| 有运行中 entry | 展示临时工时，必须等用户确认 |
| task_hours 未确认 | `notion_hours_synced: false` |
| Notion 未连接/字段变化 | 日报成功，Notion 标 pending |
| Notion 匹配为 0 或多条 | 停止写入，要求用户选择 |
| 写后验证不一致 | 标 pending，不报告成功 |
