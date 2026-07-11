# 面向 OpenAI Codex 的 Reduce Critical Unknowns

[![Validate Skill](https://github.com/dudaxing/know-your-unknowns-skill/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/dudaxing/know-your-unknowns-skill/actions/workflows/validate-skill.yml)

一套 evidence-first、风险相称的 Agent Skill：尽早发现并用廉价证据处理那些会改变软件设计、实现、发布或验证方式的未知量。

[English README](README.md)

> 仓库名为保持链接连续性暂不更改；主要 Skill 已更名为 `reduce-critical-unknowns`，目标平台是 OpenAI Codex。

目录遵循 OpenAI 当前的 [Build skills](https://learn.chatgpt.com/docs/build-skills) 规范：在 `.agents/skills` 下发现仓库 Skill、frontmatter 只保留两个字段、使用 progressive disclosure，并提供 `agents/openai.yaml` UI metadata。

## 这次更新改变了什么

旧版本围绕 11 个 technique 和交互页面组织工作。新版本保留有工程价值的行为，删除固定媒介与仪式：

- 先查代码、测试、历史、配置、schema 和运行行为，再问宽泛问题；
- 只处理会改变下一项决定的未知量；
- 默认只运行一个最便宜、可信、最可能改变决定的探针；
- 每个探针都说明目标决定、所需证据和停止条件；
- 对局部、可逆的选择采用保守默认并继续；
- 对高影响、证据弱、难回滚的问题，只暂停受影响分支；
- 把结果折回实现、测试、rollout 或简短的人类选择；
- 风险足以继续时停止，而不是穷尽所有未知量。

运行时 Skill 不要求页面工件、canonical unknowns ledger、风险乘法、固定阶段 gate 或 `.skill` 分发归档。

## 适用场景

- 陌生的认证、权限、session 或迁移工作；
- 跨独立部署 consumer 的 schema 与公共契约变更；
- 跨语言、跨运行时的语义移植；
- 会改变架构或数据边界的模糊重要功能；
- 实现时发现计划前提错误；
- rollout、rollback 或 observability 决策；
- 大型或高风险 diff 的独立合并前验证；
- 显式请求盲点扫描、假设审计、聚焦访谈、小型 spike、语义地图、偏差分流或证据复核。

文档错字、格式化、局部变量改名和规格明确的可逆小修不应启动完整流程。即使显式调用 Skill，也最多保留一个真正重要的假设，然后正常实现。

## 安装

### 直接在本仓库使用

克隆仓库，并在仓库根目录或其子目录中启动 Codex。Codex 会发现 `.agents/skills/reduce-critical-unknowns`。

```bash
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
cd know-your-unknowns-skill
```

### 安装到其他仓库

把 Skill 文件夹复制到目标仓库的 `.agents/skills/`：

```powershell
$source = ".agents\skills\reduce-critical-unknowns"
$target = "C:\path\to\your-repo\.agents\skills\reduce-critical-unknowns"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
Copy-Item -Recurse -Force $source $target
```

```bash
mkdir -p /path/to/your-repo/.agents/skills
cp -R .agents/skills/reduce-critical-unknowns /path/to/your-repo/.agents/skills/
```

### 安装到当前用户

把同一文件夹复制到 `$HOME/.agents/skills/reduce-critical-unknowns`。

## 调用示例

```text
$reduce-critical-unknowns 为旧认证模块增加 rotating sessions；在启用新写入前验证迁移与回滚前提。
```

```text
$reduce-critical-unknowns 把 Rust retry controller 移植到 TypeScript，保留调用方可观察的时序、错误、重试与取消语义。
```

```text
$reduce-critical-unknowns 检查这个大型 diff 的合并准备度，把验收、回滚、观测与失败路径映射到证据。
```

任务匹配 frontmatter description 时，Codex 也可以隐式选择该 Skill。

## 行为模型

| 情况 | 预期行为 |
|---|---|
| 清晰、局部、可逆的小修 | 检查局部上下文，最多记录一个重要假设，直接实现并运行聚焦验证。 |
| 重要但仓库可以回答的未知量 | 先查最强证据，只运行一个聚焦探针，再决定是否提问。 |
| 必须由人选择、影响高且难回滚 | 展示已查证据和少量真正不同的选项，只暂停受影响分支。 |
| 实现证据推翻计划 | 记录“原前提 → 观察证据 → 决策影响 → 保守处理或升级”。 |
| 大型或高风险 diff | 将验收映射到证据，并检查失败路径、rollback、observability 和维护者心智模型。 |
| 无法访问仓库 | 说明证据缺口，把内容限制为假设和第一个可区分路径的探针。 |

详细探针和领域风险只在需要时从两个 reference 加载。

## 仓库结构

```text
.agents/skills/reduce-critical-unknowns/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── probe-playbook.md
    └── risk-patterns.md

evals/reduce-critical-unknowns/
├── trigger-cases.json
├── behavior-scenarios.md
├── forward-test-results.md
├── results.md
└── run_static_checks.py
```

运行时 Skill 只有 4 个文件；评测、验证记录和仓库文档均位于 Skill 外，保持 progressive disclosure。

## 验证

```bash
python -m pip install PyYAML==6.0.3
python -m py_compile evals/reduce-critical-unknowns/run_static_checks.py
python evals/reduce-critical-unknowns/run_static_checks.py
```

同时使用当前 Codex `$skill-creator` 自带的 `quick_validate.py` 验证 `.agents/skills/reduce-critical-unknowns`。

当前基线：

- 25 条触发语料，覆盖正例、显式请求、立即实现、近邻负例和明确负例；
- 8 个行为场景，共 54 条可观察 assertions；
- 显式独立 forward-test 为 54/54；
- 因测试环境不暴露 Skill-load trace，尚未声称真实隐式触发率。

详见[验证结果](evals/reduce-critical-unknowns/results.md)与[行为评测结果](evals/reduce-critical-unknowns/forward-test-results.md)。

## 从旧版本迁移

- 显式调用名从 `$know-your-unknowns` 改为 `$reduce-critical-unknowns`。
- 安装新 Skill 前删除旧版本；同时保留两者可能造成重叠触发。
- 旧 `dist/know-your-unknowns.skill` 已删除，以 `.agents/skills/` 中的 Codex-native 目录为唯一事实源。
- 历史 technique 名仍会映射到最小匹配探针，但不再强制旧输出媒介、固定数量或门禁。

## 方法来源

方法受 Thariq Shihipar 的 [Know Your Unknowns 指南与配套示例](https://thariqs.github.io/html-effectiveness/unknowns/)以及本仓库旧实现启发。本次版本为 OpenAI Codex 重新综合工程行为，没有复制旧展示层。
