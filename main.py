import json
import os
import django

# Konfiguracja Django, jeśli uruchamiasz plik niezależnie
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import Race, Guild, Skill, Player


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        race_name = player_data.get("race")
        race, _ = Race.objects.get_or_create(name=race_name)

        guild_name = player_data.get("guild")
        guild_description = player_data.get("guild_description", "")
        guild = None
        if guild_name:
            guild, _ = Guild.objects.get_or_create(
                name=guild_name, defaults={"description": guild_description}
            )

        skill_objects = []
        for skill_info in player_data.get("skills", []):
            skill_name = skill_info.get("name")
            skill_bonus = skill_info.get("bonus", "")
            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                defaults={"bonus": skill_bonus, "race": race},
            )
            skill_objects.append(skill)

        player, _ = Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
            },
        )

        player.skills.set(skill_objects)
        player.save()


if __name__ == "__main__":
    main()
