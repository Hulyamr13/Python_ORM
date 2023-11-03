from django.db import models


class RechargeEnergyMixin:
    def recharge_energy(self, amount):
        self.energy = min(self.energy + amount, 100)
        self.save()
        return self.energy


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class SpiderHero(Hero):
    def swing_from_buildings(self):
        if self.energy >= 80:
            self.energy -= 80
            self.save()
            return f"{self.name} as Spider Hero swings from buildings using web shooters"
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    class Meta:
        proxy = True


class FlashHero(Hero):
    def run_at_super_speed(self):
        if self.energy >= 65:
            self.energy -= 65
            self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    class Meta:
        proxy = True
