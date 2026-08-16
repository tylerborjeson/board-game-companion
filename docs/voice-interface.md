# Voice interface

Wispr Flow supplies dictation **outside** this repository. Alpha accepts text, not audio.

## Intended path

```text
Tyler speaks into Wispr Flow
  → text appears in a local UI or CLI
  → Tyler presses Enter / submits
  → companion.handle_turn interprets the whole submitted turn
  → Noko answers in short, listen-friendly prose
```

## Optimize for

- Natural, messy speech
- Long dictated turns with multiple actions and observations
- An explicit submit boundary (do not stream partial sentences into state)
- Clear separation between intended action and reported physical result
- Short spoken replies
- A full structured/debug object when needed

## Do not

- Couple phase changes to a microphone
- Require one sentence per action
- Build STT/TTS in alpha

Future speech-to-speech can call the same `TurnInput` / `TurnOutput` contract.
