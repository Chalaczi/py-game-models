from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:  # dodana adnotacja typu
        return self.name


class Guild(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # dodana adnotacja typu
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bonus = models.TextField(blank=True, default="")

    def __str__(self) -> str:  # dodana adnotacja typu
        return self.name


class Player(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True, default="")
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self) -> str:  # dodana adnotacja typu
        return self.nickname
