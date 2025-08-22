import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    """Wczytuje dane z players.json i dodaje je do bazy danych."""
    with open("players.json", "r") as f:
        data = json.load(f)

    for player_data in data:
        # Jeśli player_data jest stringiem, ignorujemy go lub wypisujemy ostrzeżenie
        if not isinstance(player_data, dict):
            print(f"Nieprawidłowy format gracza: {player_data}")
            continue

        # Tworzenie lub pobranie rasy
        race_name = player_data.get("race")
        if not race_name:
            print(f"Gracz {player_data.get('nickname')} nie ma podanej rasy, pomijam.")
            continue

        race, _ = Race.objects.get_or_create(name=race_name)

        # Tworzenie lub pobranie gildii
        guild_name = player_data.get("guild")
        guild = None
        if guild_name:
            guild_description = player_data.get("guild_description") or None
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
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
            if not isinstance(skill_data, dict):
                print(f"Nieprawidłowy format umiejętności dla gracza {player.nickname}: {skill_data}")
                continue

            skill_name = skill_data.get("name")
            if not skill_name:
                continue

            power = skill_data.get("power", 0)
            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                race=race,
                defaults={"power": power},
            )
            player.skills.add(skill)


if __name__ == "__main__":
    main()
