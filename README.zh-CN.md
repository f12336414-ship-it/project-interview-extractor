# Project Interview Extractor

一个证据优先的 Codex Skill：把真实软件项目材料整理为可用于面试的项目介绍、项目化问题、追问链、简历亮点和 STAR 案例，同时避免编造经历。

[English](README.md)

## 核心能力

- 区分已确认事实、单一来源信息、合理推断和假设建议。
- 从业务、职责、架构、选型、数据、接口、性能、稳定性、安全和工程化等维度分析项目。
- 根据真实模块和技术链路生成问题，而非只问框架八股。
- 进行一次一题、根据回答动态追问的模拟面试。
- 在不扩大职责、不虚构指标的前提下优化简历与 STAR 表达。

## 四种模式

| 模式 | 用途 |
|---|---|
| 快速模式 | 快速获得项目介绍、高频问题、重点追问和亮点候选 |
| 深度模式 | 生成完整项目面试经验报告 |
| 模拟面试模式 | 一次一题训练表达，并根据回答继续追问 |
| 简历优化模式 | 生成证据边界清晰的简历描述和面试风险提示 |

## 安装

克隆仓库后，将内层 `project-interview-extractor` 目录复制到 Codex Skills 目录。

### macOS 和 Linux

```bash
git clone https://github.com/f12336414-ship-it/project-interview-extractor.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R project-interview-extractor/project-interview-extractor \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-interview-extractor"
```

### Windows PowerShell

```powershell
git clone https://github.com/f12336414-ship-it/project-interview-extractor.git
$skills = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$env:USERPROFILE\.codex\skills" }
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force ".\project-interview-extractor\project-interview-extractor" "$skills\project-interview-extractor"
```

## 使用

Codex 的斜杠命令是产品内置会话控制。本项目通过 `$project-interview-extractor` 提供跨 App、CLI 和 IDE 可移植的 Skill 子命令；也可以先用 `/skills` 选中 Skill，再输入子命令。

| 命令 | 用途 |
|---|---|
| `help` | 显示命令、参数、默认值和示例 |
| `chat` | 一次一题进行贴近真实面试的动态对练 |
| `bank` | 把全维度问题、追问和回答写入 Markdown 学习文档 |
| `analyze` | 快速或深度分析项目 |
| `resume` | 生成证据边界清楚的简历内容 |
| `review` | 评估候选人最近一次回答 |
| `export` | 导出当前会话或报告 |

进行真实模拟面试，结束后统一反馈：

```text
$project-interview-extractor chat --role backend --level senior --rounds 12 --feedback end
```

生成供开发者系统学习的全维度题库文档：

```text
$project-interview-extractor bank --role backend --level senior --coverage exhaustive --output docs/backend-interview-bank.md
```

可以提供 README、源码目录、简历描述、架构文档、接口或数据库文档、Git 记录、核心代码或口述背景。材料不足时，Skill 会继续基于已有证据分析，同时明确标记待确认信息。

`bank` 会检查 17 个维度，对不适用维度给出理由，并写入项目化问题、保守版回答、三层追问、风险、学习导读和自测清单。“所有维度”是可验收的覆盖标准，而不是声称穷举无限种问法。

## 验证

```bash
python scripts/validate_repository.py
```

验证脚本不依赖第三方 Python 包。行为评测的范围和限制见 [评测说明](docs/EVALUATION.md)。

## 参与贡献

提交贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。公开 Issue 中不要粘贴凭据、个人隐私或未授权的项目材料；安全问题请遵循 [SECURITY.md](SECURITY.md)。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。
