# Hermes integration

The Hermes campaign guide can use this repository as the home for shared schemas, documentation, and future API adapters.

Keep the live campaign ledger outside the public repository unless it has been intentionally sanitized.

The integration contract is:

1. read the current state
2. ask the player to confirm physical state
3. propose a command
4. validate and apply it through the game core
5. narrate the resulting events
6. persist the new state

Do not include copyrighted rulebook text or card assets in this repository.
