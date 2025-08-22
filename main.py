import json
from db.models import Race, Guild, Skill, Player


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        race_name = player_data["race"]
        race, _ = Race.objects.get_or_create(name=race_name)

        guild_name = player_data.get("guild")
        guild = None
        if guild_name:
            guild_description = player_data.get("guild_description") or ""
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description},
            )

        player, _ = Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
            },
        )

        for skill_data in player_data.get("skills", []):
            skill_name = skill_data["name"]
            bonus = skill_data.get("bonus", "")
            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                defaults={"bonus": bonus, "race": race},
            )
            player.skills.add(skill)


if __name__ == "__main__":
    main()
