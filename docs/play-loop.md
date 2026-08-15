# play loop

Shared loop for every game. Voice and sources come from `games/<game>/`.

1. confirm the current physical state
2. narrate 2–5 sentences of fiction
3. identify the phase and legal actions
4. explain the relevant rule
5. apply it to this board
6. offer mentor advice without choosing
7. wait for the player's action and result
8. update the active `state.json`; put story in `notes.md`
9. narrate the consequence
10. stop at the next unresolved decision

Active Arkham table: `games/arkham-horror/campaigns/night-of-the-zealot/scenarios/the-midnight-masks/state.json`

The physical tabletop remains authoritative whenever it conflicts with stored state.
