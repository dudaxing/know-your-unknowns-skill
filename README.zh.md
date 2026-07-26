# know-your-unknowns（知你所不知）

*一个 Claude Code skill：在代价变得昂贵之前，发现你不知道自己不知道的东西。*

[English README](README.md)

基于 Anthropic 工程师 Thariq Shihipar 的 **"Know Your Unknowns" field guide** 及其[配套 HTML 演示](https://thariqs.github.io/html-effectiveness/unknowns/)。核心前提：**地图非疆域。**"地图"是你交给 AI agent 的一切——prompt、计划、假设；"疆域"是真实的代码库、它的历史、未写成文档的约束、以及需求背后的真实意图。两者之间的落差就是你的 unknowns。本 skill 的全部技术都为同一个目的存在：**主动地、廉价地关闭这个落差，而不是通过返工被动地发现它。**

## 内容概览

**11 项技术**覆盖开发全生命周期，每项按"最快消解未知"的原则选择交付媒介——比较、mock、计划、测验用**自包含交互式 HTML artifact**；unknowns scan、访谈、实现笔记日志走纯聊天或 markdown——外加一个横切政策层：即使没有触发任何具体技术，它也为一切非平凡任务提供默认行为。

### 四类未知

|  | 你知道它 | 你不知道它 |
|---|---|---|
| **有意识** | 已知的已知——已写进 prompt | **已知的未知**——你清楚尚未解决的开放问题 |
| **无意识** | **未知的已知**——说不出口但一眼能认出的品味/经验 | **未知的未知**——你根本没想到要问的 |

### 11 项技术

| # | 阶段 | 技术 | 猎取目标 | 触发示例 |
|---|------|------|----------|----------|
| 1 | 实现前 | **盲区扫描**——扫描陌生代码与 git 历史，以卡片形式报告地雷，附可复制的 prompt 修正 | 未知的未知 | "blindspot pass"、"盲区扫描" |
| 2 | 实现前 | **教我我的未知**——交互式领域讲解，词汇阶梯 + 实时控件 | 缺失的专业词汇 | "teach me my unknowns"、"教我我的未知" |
| 3 | 实现前 | **设计方向**——同一份数据渲染 3–5 种互不兼容的设计哲学，steal/skip 选择芯片 | 未知的已知（品味） | "design directions"、"出几个设计方向" |
| 4 | 实现前 | **先 mock 再接线**——假数据的抛弃式可点击原型 + A/B 问题 | 未知的已知（交互偏好） | "mock it first"、"做个原型看看" |
| 5 | 实现前 | **头脑风暴干预点**——约 10 个扎根于代码库现状的方案，从最便宜到最激进 | 方案空间 | "brainstorm interventions" |
| 6 | 实现前 | **访谈**——一次一题，按架构爆炸半径排序 | 已知的未知 | "interview me"、"访谈我" |
| 7 | 实现前 | **指向参照物**——移植前先产出语义地图证明理解，签核门禁通过才动手 | 能认出但说不出的行为 | "semantics map"、"照着这个实现" |
| 8 | 实现前 | **可调计划**——按"你多可能改它"排序而非执行顺序，机械工作折叠，明确 go/no-go | 最可能被改的决策 | "tweakable plan"、"可调计划" |
| 9 | 实现中 | **实现笔记**——带时间戳的日志，记录每次计划偏差与保守选择 | 途中发现的未知 | "keep implementation notes"、"记录实现笔记" |
| 10 | 实现后 | **Buy-in 文档**——demo 先行、预答异议并链接证据、点名签核人 | 评审者的未知 | "buy-in doc"、"打包给评审" |
| 11 | 实现后 | **合并前测验**——合并就绪报告 + 六题理解测验，全对才解锁清单 | 你自己对变更的未知 | "quiz me"、"考考我" |

### 它是"被点名才用的工具箱"，不是默认编排器

这个 skill 只在你点名要它的某项技术时才运行，不会插进日常工作——你说"加个 CSV 导入"，得到的就是 CSV 导入，不是一套发现流程。它也**让位而非抢活**：一般文档、方案、RFC 归文档类 skill；UI 设计与建造归设计类 skill；代码正确性审查归审查类 skill。工作重叠时，本 skill 只产出结构化输入（决策表、选定的方向、交互契约），成品交给对方。

唯一默认运行的是下面那个 compact unknowns scan：几行字，不产出 artifact，不打断你。

### 横切政策层

[references/scan-and-policies.md](know-your-unknowns/references/scan-and-policies.md) 为非平凡任务提供的默认行为：

- **Unknowns scan**——开工前 compact 四类未知分类扫描，以「建议下一步」与 **Suggested trigger phrase（可复制触发句）** 收尾。
- **问答决策政策（ask-vs-decide）**——实现前与实现中共用同一条判据：是否存在**不丢数据、不放宽访问权限**的保守方案？有，就采用它、记录、显著标记，然后继续；如果任何可行方案都做不到，就停下来问你——那种决定本来就该由你做。
- **疆域检查清单**——feature flags、迁移、legacy 数据、被 revert 的 PR、环境差异、既有工具、评审者预期。
- **14 条须规避的失败模式**——例如"复制最相似的文件而不检查它是否是个例外"、"把 dev/staging 行为当生产真相"、"把单测通过当权限安全的证明"。

### 招牌交互：reply builder

每个需要用户做决策的 artifact 都以 **reply builder** 收尾：steal/skip 芯片、"这个有共鸣"复选框、A/B 单选会实时汇聚成一段结构化、可一键复制的回复，粘贴回对话即可。*做出反应比凭空想象容易*——用户只需点击而不必组织语言，agent 收到的是结构化输入而非散文。实现了全部交互机制的可复用骨架见 [assets/artifact-skeleton.html](know-your-unknowns/assets/artifact-skeleton.html)。

## 安装

每个宿主**只装一个位置**，不要维护多份副本。下面列出的都是各宿主**自己的原生路径**（不是兼容层）：

| 宿主 | 用户级 | 项目级 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |

某个宿主可能额外加载别的宿主的路径（取决于版本与设置）——那是附带效果，不要当作正式安装位置来写。

```bash
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
cp -r know-your-unknowns-skill/know-your-unknowns ~/.claude/skills/     # Claude Code
# 或 ~/.cursor/skills/   （Cursor）
# 或 ~/.agents/skills/   （Codex）
```

Windows（PowerShell）——把目标目录换成你的宿主：

```powershell
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
Copy-Item -Recurse know-your-unknowns-skill/know-your-unknowns "$env:USERPROFILE\.claude\skills\"
```

改装到项目级：

```powershell
New-Item -ItemType Directory -Force "$PWD\.cursor\skills" | Out-Null
Copy-Item -Recurse .\know-your-unknowns "$PWD\.cursor\skills\"
```

安装或更新后，**新开一个聊天**是稳妥做法。Claude Code 会在会话内感知已知 skills 目录里的改动；但如果某个 skills 根目录在会话开始时并不存在，则需要重启。

验证：*"对 auth 模块做一次盲区扫描"* 或 *"就导出功能访谈我"*。HTML 工件用浏览器打开 `file://`；scratch 路径与 info/exclude 规则在所有宿主上一致适用。

### 打包版 `.skill` 文件

面向接受 skill 上传的平台：到 [Releases 页面](https://github.com/dudaxing/know-your-unknowns-skill/releases)下载 `know-your-unknowns.skill`——每个打了 tag 的版本都由 CI 从该提交现场构建并附上。

也可以自己构建：

```bash
python scripts/build_skill.py
```

它会先校验 skill，再写出 `dist/know-your-unknowns.skill`。纯标准库、无需参数，在 Windows 上也不用设编码环境变量。构建是**字节可复现**的：同样的源码永远产出同样的归档，所以想确认某个副本是不是过期的，重新构建比对即可。

这个归档**刻意不提交进仓库**。构建产物和源码放在一起，第一次有人改了 reference 却忘记重新打包就会失步，而且因为是二进制，评审时看不出来。`python scripts/build_skill.py --check` 跑的是 CI 每次推送都会跑的那套校验：frontmatter 与描述长度上限、内部链接完整性、以及对本机绝对路径和"伸手进别的 skill 安装目录"的扫描。

## 如何用这套 skill 科学地设计代码

**地图 ≠ 疆域。** 先花小成本关闭 unknowns，再让 agent 写代码。

1. **说清任务** — 若未指定技巧，agent 会先跑 compact **Unknowns scan**（四类未知 + 建议下一招 + **可复制触发句**）。
2. **选对技巧** — 见上表；显式触发优先（如「访谈我」「盲区扫描」）。
3. **反应式工件** — 比较/布局/测验类产出为单文件 HTML；在页面底部用 reply builder 复制结构化回复，**粘贴回对话**。
4. **折入下一轮** — 每个 artifact 都带一个 id，回复以 `Artifact: KYU-EXAMPLE` 开头，使粘贴回来的决定能归属到**那一份** artifact，而不会与文档里的引用、旧 artifact 的重放、或上下文里的回声混淆。agent 按整行解析白名单字段，先更新计划再行动。三道检查点：移植前 `semantics confirmed`、实现前 `Go: approve`、合并前由 agent 判卷的 `Q<n>:` 满分（粘贴的 `Quiz score:` 不算结果）。
5. **新会话实现** — 计划通过后 **新开 Agent 会话**，只附带计划、决策表、mock/语义地图与 `implementation-notes.md` 路径（见 SKILL.md handoff）。
6. **实现中** — 用实现笔记记录偏差；**实现后** — buy-in 文档 / 合并前测验按需选用。

典型可选链路：盲区 → 访谈 → 可调计划 → 实现笔记 → buy-in → 合并测验。**工具箱，非流水线。**

## 与 Thariq 博客演示的对照

| 博客演示 | 本 skill 参考 |
|----------|----------------|
| [01 Blindspot pass](https://thariqs.github.io/html-effectiveness/unknowns/01-blindspot-pass.html) | [blindspot-pass.md](know-your-unknowns/references/blindspot-pass.md) |
| [02 Teach me / color grading](https://thariqs.github.io/html-effectiveness/unknowns/02-color-grading-explainer.html) | [teach-me.md](know-your-unknowns/references/teach-me.md) |
| [03 Four design directions](https://thariqs.github.io/html-effectiveness/unknowns/03-design-directions.html) | [design-directions.md](know-your-unknowns/references/design-directions.md) |
| [04 Mock before you wire](https://thariqs.github.io/html-effectiveness/unknowns/04-toolbar-mock.html) | [mock-first.md](know-your-unknowns/references/mock-first.md) |
| [05 Brainstorm interventions](https://thariqs.github.io/html-effectiveness/unknowns/05-churn-brainstorm.html) | [brainstorm-interventions.md](know-your-unknowns/references/brainstorm-interventions.md) |
| [06 The interview](https://thariqs.github.io/html-effectiveness/unknowns/06-interview.html) | [interview.md](know-your-unknowns/references/interview.md) |
| [07 Point at a reference](https://thariqs.github.io/html-effectiveness/unknowns/07-reference-port.html) | [reference-port.md](know-your-unknowns/references/reference-port.md) |
| [08 Tweakable plan](https://thariqs.github.io/html-effectiveness/unknowns/08-implementation-plan.html) | [tweakable-plan.md](know-your-unknowns/references/tweakable-plan.md) |
| [09 Implementation notes](https://thariqs.github.io/html-effectiveness/unknowns/09-implementation-notes.html) | [implementation-notes.md](know-your-unknowns/references/implementation-notes.md) |
| [10 Buy-in doc](https://thariqs.github.io/html-effectiveness/unknowns/10-pitch-doc.html) | [buy-in-doc.md](know-your-unknowns/references/buy-in-doc.md) |
| [11 Merge quiz](https://thariqs.github.io/html-effectiveness/unknowns/11-change-quiz.html) | [merge-quiz.md](know-your-unknowns/references/merge-quiz.md) |

博文：[Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns) · 演示索引：[unknowns 配套站](https://thariqs.github.io/html-effectiveness/unknowns/)

## 使用示例

```text
我从没碰过这个代码库的支付模块。在我让你加退款流程之前，先做一次盲区扫描。
```

```text
就导出功能访谈我，一次一个问题，优先问答案会改变架构的。
```

```text
这个 Rust crate 的退避行为正是我们要的。先做语义地图，我回复"semantics confirmed"你再动手移植。
```

```text
出几个设计方向让我挑，同一份数据，风格差异要大，带 steal/skip 选项。
```

```text
给这个 diff 生成合并就绪报告，最后带一个我必须通过的测验。
```

技术之间自然串联——典型的完整功能流：盲区扫描 → 访谈 → 可调计划 → 实现笔记 → buy-in 文档 → 合并测验。但这是**工具箱，不是流水线**：skill 只运行当前主导未知所需要的那部分。

## 仓库结构

```
know-your-unknowns/            skill 本体（安装到某一个宿主 skill 根，如 .cursor/skills/ 或 ~/.claude/skills/）
├── SKILL.md                   核心：原则、技术选型表、工作流（约 120 行）
├── references/                按需加载，每项技术一个文件
│   ├── scan-and-policies.md   横切：unknowns scan、ask-vs-decide、失败模式
│   ├── artifact-patterns.md   HTML artifact 构建规范 + reply-builder 说明
│   ├── blindspot-pass.md      …… 到 ……
│   └── merge-quiz.md          （共 11 个技术文件）
├── evals/
│   └── smoke-triggers.md      触发句 → 期望行为验收用例
└── assets/
    └── artifact-skeleton.html 可复用单文件骨架：芯片、复选框、reply builder
scripts/
└── build_skill.py             校验 + 构建 .skill 归档（纯标准库）
.github/workflows/
├── validate.yml               每次推送跑校验
└── release.yml                打版本 tag 时构建并附到 Release
```

`dist/` 是构建输出，不纳入版本控制；需要时运行 `python scripts/build_skill.py` 生成。

布局遵循**渐进披露**原则：常驻上下文的只有 frontmatter 描述（约 1.3 KB，含中英文触发词）；SKILL.md 正文在触发时加载；每项技术的参考文件只在该技术运行时加载。用一项技术永远不必为另外十项付出上下文代价。

## 设计脉络

本 skill 融合了三个来源，各取其长：

1. **[Thariq 配套演示](https://thariqs.github.io/html-effectiveness/unknowns/)**（主体）——完整的 11 项技术及其交互深度：盲区七类模式、语义地图的"承重细节"标注法、reply-builder 机制。
2. **[GreatMark/fable-field-guide-skills](https://github.com/GreatMark/fable-field-guide-skills)**——行为规则（先锚定用户起点；访谈每题给推荐项；至少一个设计方向要超出用户既有品味）与工件卫生（scratch 目录、git info/exclude、脚手架不进 changeset）。
3. **一个 `unknowns-driven-development` 变体**——横切政策层：默认 unknowns scan、ask-vs-decide 政策、失败模式清单。

## 许可证

[MIT](LICENSE)。方法论属于 Thariq Shihipar 且已公开发表；本仓库是把它实现为 agent skill 的独立作品，MIT 授权覆盖的是这份实现。

## 致谢

方法论来自 [Thariq Shihipar](https://thariqs.github.io/)（Anthropic）的 "Know Your Unknowns" field guide 与 HTML-effectiveness 配套演示。本仓库是面向 AI 编码 agent 的独立 skill 实现。
