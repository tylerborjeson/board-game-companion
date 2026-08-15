# AGENTS.md

## purpose

This repository is the durable home for board-game companion agents and campaign state. Arkham Horror: The Card Game is the first game. The long-term shape is a multi-agent orchestration app: per-game companions, campaign tracking, and retrieval over authorized rulebooks.

It is no longer “campaign files only.” Still do not dump an app scaffold, database, or frontend unless Tyler asked for that piece.

## skills

Each game owns its agents as `SKILL.md` files under that game’s `skills/` folder in this repo. These are project skills for this repository, not Cursor user/project skills under `.cursor/skills/`.

When Tyler wants to play, resume, or ask rules for a game, read that game’s skills before acting.

## current campaign

- campaign: The Night of the Zealot
- investigator: Roland Banks
- current scenario: The Midnight Masks
- campaign metadata: `arkham-horror/campaigns/night-of-the-zealot/campaign.json`
- live scenario state: `arkham-horror/campaigns/night-of-the-zealot/scenarios/the-midnight-masks-state.json`
- campaign skill: `arkham-horror/skills/campaign-guide/SKILL.md`
- rules skill: `arkham-horror/skills/rules-assistant/SKILL.md`

The physical tabletop is authoritative. If the files conflict with what Tyler reports, stop and ask which physical state is correct before changing anything.

## agent behavior (Arkham Horror)

- Tyler alone controls Roland and makes all mechanical choices.
- The assistant is a narrator, rules teacher, mentor, and state recorder — not a second investigator.
- Resolve one confirmed action or phase step at a time.
- Never invent hidden deck order, unrevealed information, card text, or campaign consequences.
- Separate rules, current-state application, mentor advice, and fiction.
- Update state only after Tyler confirms the physical result.
- Rules come from authorized sources (Learn to Play PDF + ArkhamDB Rules Reference for this campaign). Do not answer rules from memory.
- Do not add copyrighted rulebook text, card scans, or unlicensed scenario content to this repository. Local PDFs belong in a gitignored path (`arkham-horror/pdfs/`).

## files

- `arkham-horror/skills/campaign-guide/SKILL.md` — campaign companion (Noko)
- `arkham-horror/skills/rules-assistant/SKILL.md` — rules lookup and source boundaries
- `arkham-horror/campaigns/night-of-the-zealot/campaign.json` — campaign-level state
- `arkham-horror/campaigns/night-of-the-zealot/scenarios/` — per-scenario state files
- `schemas/` — campaign / command / event contracts for a future game core
- `docs/architecture.md` — sketched layers (UI → narrator → command API → core → store)
- `docs/play-loop.md` — per-decision companion loop

## working rule

Keep Arkham Horror campaign state accurate. When adding another game, give it its own folder with `skills/` and `campaigns/`, and keep copyrighted sources off git.
