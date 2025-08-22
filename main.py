import json
from db.models import Race, Guild, Skill, Player

def main():
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_data in data:
        race, _ = Race.objects.get_or_create(name=player_data["race"])
        guild_name = player_data.get("guild")
        guild_desc = player_data.get("guild_description", "")
        guild = None
        if guild_name:
            guild, _ = Guild.objects.get_or_create(name=guild_name, defaults={"description": guild_desc})

        player, _ = Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild
            }
        )

        for skill_data in player_data.get("skills", []):
            skill, _ = Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={
                    "bonus": skill_data.get("bonus", ""),
                    "race": race
                }
            )
            player.skills.add(skill)
