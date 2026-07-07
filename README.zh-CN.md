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

```text
使用 $project-interview-extractor 深度分析这个项目，帮我准备后端项目面试。
```

可以提供 README、源码目录、简历描述、架构文档、接口或数据库文档、Git 记录、核心代码或口述背景。材料不足时，Skill 会继续基于已有证据分析，同时明确标记待确认信息。

## 验证

```bash
python scripts/validate_repository.py
```

验证脚本不依赖第三方 Python 包。行为评测的范围和限制见 [评测说明](docs/EVALUATION.md)。

## 参与贡献

提交贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。公开 Issue 中不要粘贴凭据、个人隐私或未授权的项目材料；安全问题请遵循 [SECURITY.md](SECURITY.md)。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。
