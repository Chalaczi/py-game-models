import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        # Tworzenie lub pobranie rasy
        race_info = player_data.get("race")
        if isinstance(race_info, dict):
            race_name = race_info.get("name")
        else:
            race_name = str(race_info)
        race, _ = Race.objects.get_or_create(name=race_name)

        # Tworzenie lub pobranie gildii
        guild_name = player_data.get("guild")
        guild = None
        if guild_name:
            guild_description = player_data.get("guild_description") or None
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description},
            )

        # Tworzenie gracza
        player, _ = Player.objects.get_or_create(
            nickname=player_data.get("nickname"),
            defaults={
                "race": race,
                "guild": guild,
                "level": player_data.get("level", 1),
            },
        )

        # Tworzenie umiejętności
        for skill_data in player_data.get("skills", []):
            skill_name = skill_data.get("name")
            power = skill_data.get("power", 0)
            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                race=race,
                defaults={"power": power},
            )
            player.skills.add(skill)


if __name__ == "__main__":
    main()
