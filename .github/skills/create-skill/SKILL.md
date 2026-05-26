---
name: create-skill
description: "Create or refine a workspace-scoped skill file (SKILL.md) from a conversation workflow or methodology."
argument-hint: "What should this skill produce?"
---

# Create Skill

Use this skill when the user wants to convert a repeatable workflow, checklists, or multi-step process into a reusable `SKILL.md` file.

## When to use
- The conversation describes an existing workflow, debugging process, review checklist, or methodology.
- The user needs a workspace-scoped skill that captures a repeatable procedure.
- The task is broader than a single prompt and may include decision logic or completion criteria.

## What this skill produces
- A draft `SKILL.md` file with frontmatter and a concise description.
- A clear workflow outline with steps, decision points, and quality checks.
- Example prompts for how to invoke this new skill.
- Suggested related customizations to create next.

## Process
1. Review the conversation history and workspace context.
2. Extract the workflow:
   - step-by-step actions
   - branching or decision points
   - quality criteria or completion checks
3. Clarify ambiguity by asking:
   - What outcome should this skill produce?
   - Should it be workspace-scoped or personal?
   - Should it be a quick checklist or a full multi-step workflow?
4. Draft the skill file in the repository.
5. Validate the file location and YAML frontmatter.
6. Summarize what was created and propose related next steps.

## Quality checks
- The skill description is explicit and discoverable.
- The workflow is actionable and written as a reusable process.
- The frontmatter includes `name`, `description`, and `argument-hint`.
- The output is suitable to save as `SKILL.md`.

## Example user prompts
- "Create a skill for reviewing pull request comments and applying fixes."
- "Turn this API debugging process into a reusable skill."
- "Draft a SKILL.md that captures our release checklist workflow."

## Suggested next customizations
- Add a `.github/skills/<name>/SKILL.md` for a specific repo workflow.
- Create a matching `*.prompt.md` for a one-off task inside that workflow.
- Add `AGENTS.md` or `copilot-instructions.md` if the skill should be part of a broader agent profile.
