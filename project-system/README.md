# Project System Skill

`project-system` 是一套把代码仓库改造成 AI-native 项目记忆系统的 `skill`。

它面向长期、多轮次、可持续交接的编码工作，目标是让多个 `agent` 在同一个项目里共享：

- 稳定的项目上下文
- 基于 `task` 的执行边界
- 可持续写回的状态信息
- 可复用的 `learnings` 与 `skills`

## 功能介绍

这套 `skill` 主要解决四类问题：

1. `agent` 容易一次性读取过多上下文，导致注意力分散
2. `agent` 容易把模糊需求当成“可以随意重构整个项目”的许可
3. `agent` 完成一轮开发后不写回状态，导致下一轮上下文丢失
4. 同类问题会被反复排查，经验无法沉淀成可复用流程

对应地，这套 `skill` 提供以下能力：

1. 为新项目初始化一套项目记忆型仓库结构
2. 让 `agent` 按渐进披露方式加载上下文，而不是全量扫仓库
3. 让开发工作通过 `specs/` 与 `tasks/` 来驱动，而不是直接从自然语言需求开工
4. 要求每轮开发后把 `status`、`decisions`、`learnings`、`skills` 写回仓库
5. 让项目具备多轮开发连续性，而不是依赖当前对话窗口的临时记忆

核心结构如下：

```text
AGENTS.md
+ PROJECT.md
+ INDEX.md
+ STATUS.md
+ ROADMAP.md
+ ARCHITECTURE.md
+ specs/
+ tasks/
+ decisions/
+ learnings/
+ skills/
```

## agent 如何加载该 skill

如果运行环境支持直接加载 Codex `skill`，优先读取：

- [SKILL.md](/Users/a1021500406/private/spec-repo/project-system/SKILL.md)

如果 `agent` 是通过仓库文件手动理解这套系统，建议按下面顺序读取：

1. 先读 [README.md](/Users/a1021500406/private/spec-repo/project-system/README.md) 获取总览
2. 再读 [SKILL.md](/Users/a1021500406/private/spec-repo/project-system/SKILL.md) 获取运行协议
3. 如果要初始化项目，读取 [assets/templates](/Users/a1021500406/private/spec-repo/project-system/assets/templates) 中的模板
4. 如果要评测或优化该 `skill`，读取 [tests](/Users/a1021500406/private/spec-repo/project-system/tests) 中的测评材料

如果运行环境允许执行脚本，优先使用：

1. `scripts/init_project.py <target-repo>`
2. `scripts/new_task.py <repo> <TASK-ID> <title> --spec <SPEC-ID>`
3. `scripts/update_index.py <repo> <specs|tasks> <ID> <file>`
4. `scripts/check_writeback.py <repo> --task <relative-task-path>`

当这套 `skill` 被应用到某个目标项目仓库后，`agent` 应该按下面顺序加载目标仓库：

1. `AGENTS.md`
2. `PROJECT.md`
3. `STATUS.md`
4. `INDEX.md`
5. 当前激活的 `tasks/` 文件
6. 该 `task` 关联的 `specs/` 文件
7. 只读取该 `task` 或 `spec` 显式引用的 `architecture`、`decision`、`skill` 文档

关键原则只有一条：

`不要默认全量读取整个 repository。`

## skill 组成

### 1. 运行协议

- [SKILL.md](/Users/a1021500406/private/spec-repo/project-system/SKILL.md)
- 定义 `bootstrap`、渐进加载、执行循环、强制写回规则

### 2. 发现与触发元数据

- [agents/openai.yaml](/Users/a1021500406/private/spec-repo/project-system/agents/openai.yaml)
- 定义该 `skill` 如何被发现、如何被描述、如何触发

### 3. repository 模板

- [assets/templates](/Users/a1021500406/private/spec-repo/project-system/assets/templates)
- 提供标准项目记忆结构与各类模板文件

### 4. 自动化脚本

- `scripts/init_project.py`
- `scripts/new_task.py`
- `scripts/update_index.py`
- `scripts/check_writeback.py`

这四个脚本分别负责：

1. 初始化项目记忆型仓库
2. 从 `task template` 生成新 `task`
3. 自动新增或刷新 `INDEX.md` 中的 `spec` / `task` 条目
4. 在结束一轮开发前检查关键写回工件是否完整

### 5. 测评材料

- [tests](/Users/a1021500406/private/spec-repo/project-system/tests)
- 包含规则校验、`demo case`、`LLM judge rubric`、`agent-run harness`

## agent 在开发时如何使用该 skill

### Bootstrap

当项目还没有项目记忆系统时：

1. 优先使用 `scripts/init_project.py` 初始化根文件
2. 创建 `specs/`、`tasks/`、`decisions/`、`learnings/`、`skills/`
3. 先补齐真实项目上下文，再开始实现代码

### Execution

每轮开发都应遵循：

1. 按加载协议读取最少必要上下文
2. 从当前 `task` 出发，而不是直接从宽泛需求出发
3. 只在声明范围内修改文件
4. 完成实现后必须进行仓库写回

### Write-Back

每轮开发结束时，至少更新所有相关工件：

1. 当前 `task` 的进度与结果
2. `STATUS.md`
3. `INDEX.md`
4. 如果行为约束变化，更新关联 `spec`
5. 如果产生长期技术选择，更新 `decisions/`
6. 如果出现新的排障或交付经验，更新 `learnings/`
7. 如果该经验可以复用，新增或更新 `skills/`
8. 对本轮产物执行一次 `LLM judge` 打分，并把结果写回报告或状态工件

如果允许执行脚本，建议在结束一轮开发前运行：

`scripts/check_writeback.py`

然后必须执行一轮 `LLM judge` 评估，不能把它当成可选项。

## 这套 skill 的核心价值

它不是单纯的模板集合，而是一个给编码 `agent` 使用的项目运行系统。

它的核心价值不是“帮你开始一次”，而是：

`让第 N+1 轮开发比第 N 轮开发更稳定。`

它通过以下方式实现这一点：

1. 用 `INDEX.md` 做检索入口
2. 用 `STATUS.md` 承载短期记忆
3. 用 `specs/` 与 `tasks/` 把问题定义和执行单元分层
4. 用 `learnings/` 与 `skills/` 把一次性经验变成可复用能力
5. 用 `AGENTS.md` 约束 `agent` 的读取和写回行为

## 测评体系

本项目当前包含三层测评，以及一套更强的 `agent-run + judge` 评测框架。

从现在开始，这里的原则是：

`每轮有效开发之后，都要做一次大模型打分。`

### 1. 结构校验

目的：

- 校验 `skill` 本身以及模板引用是否自洽

相关文件：

- [tests/validate_project_system.py](/Users/a1021500406/private/spec-repo/project-system/tests/validate_project_system.py)

校验内容：

- 必需文件是否存在
- `SKILL.md` 是否包含关键运行约束
- `SKILL.md` 中引用的模板文件是否真实存在
- `openai.yaml` 是否包含必需元数据

### 2. demo case 规则评分

目的：

- 评估这套 `skill` 是否能支撑一个真实项目记忆型仓库

相关文件：

- [tests/cases/data-ai-agent/CASE.md](/Users/a1021500406/private/spec-repo/project-system/tests/cases/data-ai-agent/CASE.md)
- [tests/cases/data-ai-agent/repo-fixture](/Users/a1021500406/private/spec-repo/project-system/tests/cases/data-ai-agent/repo-fixture)
- [tests/score_data_ai_agent_case.py](/Users/a1021500406/private/spec-repo/project-system/tests/score_data_ai_agent_case.py)

当前规则评分结果：

- `100 / 100`

评分维度：

1. `structure completeness`
2. `progressive loading`
3. `spec-task discipline`
4. `write-back quality`
5. `self-bootstrapping`
6. `domain fidelity`

这层评分的特点是稳定、可重复、适合做回归校验，但它不能证明 `agent` 的真实执行效果。

### 3. LLM Judge 评估

目的：

- 评估这套 `skill` 对编码 `agent` 实际交付效果的提升程度
- 作为每轮开发后的必选评审环节，而不是阶段性抽查

相关文件：

- [tests/llm-judge-rubric.md](/Users/a1021500406/private/spec-repo/project-system/tests/llm-judge-rubric.md)
- [tests/reports/data-ai-agent-llm-evaluation.md](/Users/a1021500406/private/spec-repo/project-system/tests/reports/data-ai-agent-llm-evaluation.md)

当前 `LLM judge` 结果：

- 原始分：`72 / 80`
- 归一化分：`90 / 100`
- 结论：`Strong`

评分维度：

1. `agent bootstrapping`
2. `progressive context loading`
3. `task grounding`
4. `write-back and state persistence`
5. `learning to skill conversion`
6. `domain adaptability`
7. `operational discipline`
8. `expected agent effectiveness`

这一层关注的是“如果强编码 `agent` 长期使用该系统，真实效果是否会提升”。  
但要注意，当前这份结果仍然属于基于 `rubric` 的模型评审，不是独立 `judge` 对真实 `agent run` 结果做的盲评。

流程要求：

1. 每轮有意义的开发完成后，都要产出一份新的 `LLM judge` 评估
2. 评估结果必须保留分项得分、理由、总分、结论
3. 下一轮优化应优先围绕最低分维度展开

### 4. Agent-Run + Judge Harness

目的：

- 让 `agent` 真正运行一轮任务，再由独立 `judge` 模型基于结果打分

相关文件：

- [tests/agent-run-harness.md](/Users/a1021500406/private/spec-repo/project-system/tests/agent-run-harness.md)
- [tests/prompts/agent-run-data-ai-agent.md](/Users/a1021500406/private/spec-repo/project-system/tests/prompts/agent-run-data-ai-agent.md)
- [tests/prompts/judge-data-ai-agent.md](/Users/a1021500406/private/spec-repo/project-system/tests/prompts/judge-data-ai-agent.md)
- [tests/check_agent_run_artifacts.py](/Users/a1021500406/private/spec-repo/project-system/tests/check_agent_run_artifacts.py)
- [tests/reports/data-ai-agent-agent-run-template.md](/Users/a1021500406/private/spec-repo/project-system/tests/reports/data-ai-agent-agent-run-template.md)

这是当前最有价值的一层测评，因为它评估的不是文档“像不像”，而是：

1. `agent` 是否真的按协议加载上下文
2. `agent` 是否真的围绕 `task` 工作
3. `agent` 是否真的写回了可供下一轮使用的状态
4. 使用这套 `skill` 后，下一轮开发是否会更容易接续

这层虽然最强，但成本也最高。  
因此推荐执行策略是：

1. 每轮都做 `LLM judge`
2. 条件允许时，再补做 `agent-run + judge`

## 打分依据

本项目所有评分最终都围绕同一个核心问题：

`这套 skill 是否提升了多轮 agent 开发的实际执行质量？`

证据等级从高到低如下：

1. 最强：真实 `agent-run` 结果 + 独立 `judge` 评审
2. 中等：`LLM judge` 对 `skill + demo repo` 的评估
3. 基础：规则式结构与 `fixture` 评分

不要把结构通过或静态高分误认为真实效果已经被证明。  
真正能说明问题的，仍然是 `agent-run + judge` 这一层。

但在日常迭代里，最低要求不是结构分，而是：

`每轮必须至少完成一次 LLM judge 打分。`

## agent 如何基于本项目自迭代优化

如果一个 `agent` 要优化这套 `skill`，建议按下面流程：

1. 先阅读 `README.md`、`SKILL.md`、模板、历史评测报告
2. 找出当前最低分维度或最重要失败模式
3. 只针对该问题做小范围修改
4. 先跑结构校验
5. 再跑 `demo case` 规则评分
6. 必须更新本轮 `LLM judge` 评估
7. 条件允许时，执行完整 `agent-run + judge` 评测
8. 如果优化过程中发现新的失败模式，把它写入 `learnings/` 或新的评测报告

如果没有本轮 `LLM judge` 结果，这一轮优化视为未闭环。

## 当前建议优先优化方向

基于目前的 `LLM judge` 结果，最值得优先做的增强有：

1. 增加更强的 `end-of-task write-back` 自动化，降低漏写状态的概率
2. 增加多个不同领域的 `case`，提高 `domain adaptability` 的可信度
3. 增加真实 `agent-run` 结果样本，提升 `judge` 评测可信度
4. 增加更多 `index` 行级校验，避免字段语义漂移

## 推荐的 agent 行为

如果一个 `agent` 被要求使用或优化该 `skill`，建议遵循：

1. 不要从头重写整套系统
2. 保持 `progressive loading` 原则不变
3. 保持 `task-grounded execution` 原则不变
4. 保持 `mandatory write-back` 原则不变
5. 优先做可以提升实际评测结果的小而精修改
6. 修改理由要围绕 `agent behavior` 改进，而不是文档表面整洁度

## 简短总结

`project-system` 不是一个普通模板仓库，而是一套面向编码 `agent` 的 repository operating system。

它的目标是把项目从“依赖当前对话记忆推进”，变成“依赖仓库内结构化记忆持续推进”。
