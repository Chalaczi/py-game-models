import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        # Rasa
        race_name = player_data["race"]["name"]
        race_desc = player_data["race"].get("description", "")
        race, _ = Race.objects.get_or_create(name=race_name, defaults={"description": race_desc})

        # Gildia
        guild_name = player_data["guild"]["name"]
        guild_desc = player_data["guild"].get("description", "")
        guild, _ = Guild.objects.get_or_create(name=guild_name, defaults={"description": guild_desc})

        # Gracz
        player, _ = Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "race": race,
                "guild": guild,
            },
        )

        # Umiejętności
        for skill_data in player_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                race=race,
                defaults={"bonus": skill_data["bonus"]}
            )


if __name__ == "__main__":
    main()
