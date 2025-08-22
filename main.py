import init_django_orm  # noqa: F401
import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    # Wczytanie danych z pliku JSON
    with open("players.json", "r") as f:
        data = json.load(f)

    # Iteracja po wszystkich graczach
    for player_data in data:
        # Utworzenie lub pobranie rasy
        race_name = player_data["race"]["name"]
        race_description = player_data["race"].get("description", "")
        race, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description}
        )

        # Utworzenie lub pobranie gildii
        guild_name = player_data["guild"]["name"]
        guild_description = player_data["guild]()

