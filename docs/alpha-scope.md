# Alpha scope

## In scope

- Repository layout and honest documentation
- Canonical Noko persona
- Typed state, command, event, and turn contracts
- Runtime schema validation
- Event log, reducers, snapshot rebuild
- Campaign repository boundary
- Source manifest and retrieval **interfaces**
- Exact card-lookup boundary
- One orchestrator with referee / clerk / narrator modules
- Fixtures and tests for the twelve acceptance cases
- Text turn input suitable for Wispr Flow
- Fake model provider for offline tests
- Safe handling of ambiguity and physical corrections

## Out of scope

- Polished frontend
- Real-time voice, STT, or TTS
- Autonomous multi-agent routing
- Generic multi-game framework
- Vector database
- Hidden-deck simulation
- Campaign-guide invention
- GitHub sync as a side effect of play
- Copyrighted PDFs, card scans, or unlicensed scenario text in git
- Treating a prompt file as a runtime
- Claiming Hermes and Git are synchronized

## Honest status

Scaffolding and a local domain core exist. A production cloud-model adapter, FTS index over a private corpus, and a local UI do **not**. See `README.md`.
