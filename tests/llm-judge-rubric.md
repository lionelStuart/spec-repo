# LLM Judge Rubric For Project-System Skill

Use this rubric when a large model evaluates whether `project-system` will improve a coding agent's real execution quality on a long-running software project.

The judge should evaluate behavior, not only file presence.

## Evaluation Target

Evaluate the combined effect of:

- `SKILL.md`
- repo bootstrap templates
- demo project memory repo generated from those templates

The question is:

`If a coding agent uses this skill during real project work, how much will it improve context loading, task grounding, state persistence, and reusable learning over repeated development rounds?`

## Scoring Scale

Score each dimension from `1` to `10`.

- `1-3`: weak, mostly ineffective in practice
- `4-6`: partially useful, but likely to break in real use
- `7-8`: strong and practically useful
- `9-10`: highly effective, robust, and likely to generalize

## Dimensions

### 1. Agent Bootstrapping

Can an agent start work from this system without needing hidden chat context?

Look for:

- clear initialization path
- explicit repo skeleton
- understandable root documents
- low ambiguity when starting a new project

### 2. Progressive Context Loading

Does the system prevent context overload and guide the agent to load only what is needed?

Look for:

- explicit loading order
- index-driven retrieval
- dependency-based reading
- avoidance of whole-repo dumping

### 3. Task Grounding

Does the system force work to happen through concrete tasks rather than broad vague goals?

Look for:

- spec versus task separation
- task scope, required context, forbidden changes, acceptance, and test plan
- containment of unrelated edits

### 4. Write-Back And State Persistence

After a development round, will the next agent recover the right state from repo documents?

Look for:

- status updates
- task progress tracking
- index state changes
- spec or ADR updates when behavior changes
- no reliance on unwritten memory

### 5. Learning To Skill Conversion

Can repeated problems be promoted into durable reusable procedures?

Look for:

- explicit learnings format
- connection from incident to pattern to skill
- agent instructions to write reusable knowledge back

### 6. Domain Adaptability

Can the framework adapt to a real project domain instead of staying generic?

Look for:

- project-specific constraints
- domain-specific specs and tasks
- architecture and decisions that reflect the target system

### 7. Operational Discipline

Does the skill create good constraints for an agent under real delivery pressure?

Look for:

- narrow modification scope
- anti-pattern warnings
- execution loop clarity
- safeguards against uncontrolled refactors

### 8. Expected Agent Effectiveness

If an average strong coding agent used this system for several rounds, how much would it improve actual outcomes?

Look for:

- lower chance of context loss
- better continuity between rounds
- easier reviewability
- improved repeatability of execution

## Output Format

The judge should produce:

1. A `1-10` score per dimension
2. One concise paragraph of reasoning per dimension
3. An overall score out of `100`
4. A short verdict:
   - `Not Ready`
   - `Useful But Fragile`
   - `Strong`
   - `Production-Worthy`

## Important Judge Constraint

Do not give full credit just because the documents exist.

Reward only if the documents form a coherent working system that would likely improve real agent behavior across multiple development rounds.
