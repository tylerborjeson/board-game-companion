from __future__ import annotations

from board_game_companion.campaign.repository import CampaignRepository
from board_game_companion.interfaces.schemas import validate_file


def validate_active_campaign(repository: CampaignRepository | None = None) -> None:
    repo = repository or CampaignRepository()
    validate_file("campaign.schema.json", repo.campaign_path)
    validate_file("scenario-state.schema.json", repo.active_state_path())


def main() -> None:
    validate_active_campaign()
    repo = CampaignRepository()
    campaign = repo.load_campaign()
    state = repo.load_active_state()
    print(f"{campaign.campaign} / {state.scenario} / {state.phase} / round {state.round}")
    print("local core ready; no cloud provider is configured")


if __name__ == "__main__":
    main()
