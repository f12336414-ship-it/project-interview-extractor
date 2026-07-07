# 子命令协议

## 目录

- 调用格式
- 通用参数
- help
- chat
- bank
- analyze
- resume
- review
- export
- 文件写入规则
- 错误处理
- 示例

## 调用格式

使用 Skill 调用而非伪造自定义斜杠命令：

```text
$project-interview-extractor <command> [--option value]
```

用户通过 `/skills` 选中本 Skill 后，也接受省略 Skill 名称的形式：

```text
chat --role backend --level senior
```

命令和枚举值使用英文，项目材料与自然语言说明可使用中文。参数次序不影响语义。明确命令优先于自动模式推断。

## 通用参数

| 参数 | 可选值/格式 | 默认值 | 作用 |
|---|---|---|---|
| `--role` | `backend`、`frontend`、`fullstack`、`test`、`data`、`ai`、`sre`、`architect` | 从材料推断 | 目标岗位 |
| `--level` | `junior`、`mid`、`senior`、`staff` | `mid` | 面试深度 |
| `--language` | `zh`、`en` 或用户指定语言 | 用户当前语言 | 输出和面试语言 |
| `--focus` | `all` 或逗号分隔的维度 | `all` | 优先覆盖范围 |
| `--project` | 文件或目录路径 | 当前上下文/工作区 | 项目材料位置 |
| `--output` | 工作区内 Markdown 路径 | 按命令决定 | 文档输出位置 |
| `--overwrite` | 无值开关 | 关闭 | 允许覆盖已有输出文件 |

角色或级别未知时先根据证据推断并标记；只有该信息会实质改变任务时才询问。不得因为缺少可选参数而停止。

## help

```text
$project-interview-extractor help
```

只输出简洁的命令表、关键参数、三个常用示例，以及“这些是 Skill 子命令而非 Codex 内置斜杠命令”的说明。不要开始项目分析。

## chat

```text
$project-interview-extractor chat [--role ROLE] [--level LEVEL]
  [--rounds N] [--feedback end|inline|off] [--focus DIMENSIONS]
  [--output PATH]
```

默认值：

- `--rounds 12`
- `--feedback end`
- `--focus all`

把 `chat` 作为真实面试模拟，不是题库展示：

1. 开场用一句话说明岗位、级别、预计轮数和反馈策略。
2. 第一题要求候选人做项目介绍或核验其最核心职责。
3. 一次只输出一个问题，不同时列出子问题清单。
4. 根据上一回答中的事实、模糊点、矛盾和技术选择动态追问。
5. 按“项目概述 → 职责核验 → 核心链路 → 技术深挖 → 质量与风险 → 扩展与反思”推进；不要机械平均轮数。
6. 默认不在每轮透露评分、答案要点或教学建议，只保持面试官语气继续提问。
7. 达到轮数或用户输入“结束面试”时，输出统一复盘；`--feedback off` 时只给会话完成提示和可选导出，不给评分。

支持会话内控制词：

- `跳过`：记录一次跳过，切换到相邻主题。
- `提示`：给一个不直接泄露答案的方向提示，并在复盘中标记该题使用过提示。
- `复盘`：立即结束并生成复盘。
- `继续`：在完成既定轮数后增加一个追问主题。
- `结束面试`：立即结束。

统一复盘包含：总评、各维度得分、证据充分度、最强三项、风险三项、被追问击穿的位置、保守版回答改写和训练计划。若指定 `--output`，将会话元数据、问题、用户回答、面试官追问和复盘写入文档；聊天中仍只展示简洁结果和文件链接。

`--feedback inline` 使用逐题反馈格式后再问下一题。`--feedback off` 不评分，但仍遵守真实性和敏感信息规则。

## bank

```text
$project-interview-extractor bank [--role ROLE] [--level LEVEL]
  [--coverage core|full|exhaustive] [--answer-style concise|full]
  [--focus DIMENSIONS] [--output PATH] [--overwrite]
```

默认值：

- `--coverage full`
- `--answer-style full`
- `--focus all`
- `--output project-interview-question-bank.md`

必须生成文档，而不是把整套题库塞进聊天回复。使用 [question-bank-schema.md](question-bank-schema.md) 的结构，并满足对应覆盖门槛：

| 覆盖级别 | 规则 |
|---|---|
| `core` | 只覆盖岗位最高优先级维度，每个维度至少 3 个主问题 |
| `full` | 覆盖所有适用维度，每个维度至少 3 个主问题，高优先级维度至少 5 个 |
| `exhaustive` | 覆盖所有适用维度，每个维度至少 5 个主问题，高优先级维度至少 8 个 |

每个主问题包含面试官意图、证据状态、回答要点、保守版参考回答、三层追问、易错回答和待本人确认项。材料不足时生成可学习的回答框架并明确 `[待确认]`，不得伪造候选人的项目事实。

“所有维度”指完整检查维度清单；并不承诺枚举无限多的自然语言问题。对项目确实不适用的维度，在覆盖矩阵中写 `N/A` 和理由，不为凑数量虚构组件。

## analyze

```text
$project-interview-extractor analyze --mode quick|deep
```

`--mode` 默认 `quick`。复用快速或深度模式模板；指定 `--output` 时写入文件，否则在聊天中返回。

## resume

```text
$project-interview-extractor resume [--level LEVEL] [--output PATH]
```

生成事实边界、职责、亮点 bullet、不同级别表述和面试风险。高级版证据不足时明确拒绝升级措辞。

## review

```text
$project-interview-extractor review
```

评估当前对话中最近一条候选人回答。用户也可以同时提供问题和回答文本。没有可评估回答时，请用户粘贴回答，不猜测。

## export

```text
$project-interview-extractor export --type session|report|resume --output PATH
```

把当前对话已生成的内容整理成文档，不补写对话中没有出现的事实。`--type` 默认根据当前会话推断。

## 文件写入规则

- 只写入用户授权的工作区；路径超出工作区时先请求确认。
- 输出目录不存在时，在权限允许的范围内创建。
- 目标文件已存在且没有 `--overwrite` 时，使用 `-YYYYMMDD-HHMMSS` 后缀创建新文件并报告实际路径。
- 使用 UTF-8 Markdown，标题和目录完整，删除内部推理和未脱敏敏感值。
- 写入后检查文件存在、非空、标题层级、维度覆盖矩阵和待确认标记。
- 最终回复提供可点击文件链接和一行覆盖摘要，不重复粘贴整份文档。

## 错误处理

- 未知命令：给出最接近的合法命令和 `help` 用法，不执行猜测的高成本任务。
- 未知参数：指出参数名和合法值，不静默忽略。
- 无效枚举：列出合法值并保留用户已提供的其他参数。
- `--rounds` 非正整数：改用默认值并明确提示。
- `bank` 无法写文件：返回阻塞原因和建议路径，不假装已经导出。

## 示例

```text
$project-interview-extractor chat --role backend --level senior --rounds 15 --feedback end
```

```text
$project-interview-extractor bank --role backend --level senior --coverage exhaustive --output docs/backend-interview-bank.md
```

```text
$project-interview-extractor analyze --mode deep --project . --output docs/project-analysis.md
```
