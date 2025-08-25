import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import Race, Guild, Skill, Player


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        race_name = player_data.get("race")
        race_description = player_data.get("race_description", "")
        race, _ = Race.objects.get_or_create(
            name=race_name, defaults={"description": race_description}
        )

        guild_name = player_data.get("guild")
        guild_description = player_data.get("guild_description", None)
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

        player, created = Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
            },
        )
        if created:
            player.skills.set(skill_objects)


if __name__ == "__main__":
    main()