from django.db import models


class Race(models.Model):
    name: str = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Guild(models.Model):
    name: str = models.CharField(max_length=255, unique=True)
    description: str = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name: str = models.CharField(max_length=255, unique=True)
    bonus: str = models.CharField(max_length=255, blank=True, default="")
    race: Race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    nickname: str = models.CharField(max_length=255, unique=True)
    email: str = models.EmailField(unique=True)
    bio: str = models.CharField(max_length=255, blank=True)
    race: Race = models.ForeignKey(Race, on_delete=models.CASCADE)
    guild: Guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, null=True, blank=True)
    skills: models.ManyToManyField = models.ManyToManyField(Skill, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nickname
