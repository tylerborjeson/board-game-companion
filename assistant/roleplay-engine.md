# roleplay engine

Canonical roleplay is two files, injected verbatim, in this order:

1. `assistant/soul.md` — shared companion soul and reply shape
2. `games/<current-game>/persona.md` — this game’s character

Do not summarize those files into a new prompt. Cursor, Hermes, and a future app should load the same text. Same model + those two files = the same feel.

Session shape, invariants, and portability rules live in `soul.md`. Voice, phrases, and examples live in `persona.md`.
