from django.db import models


class RechargeEnergyMixin:
    def recharge_energy(self, amount):
        self.energy = min(self.energy + amount, 100)
        self.save()


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class SpiderHero(Hero):
    def swing_from_buildings(self):
        if self.energy <= 0:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        else:
            self.energy -= 80
            if self.energy <= 0:
                self.energy = 0
            self.save()
            return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True


class FlashHero(Hero):
    def run_at_super_speed(self):
        if self.energy <= 0:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        else:
            self.energy -= 65
            if self.energy <= 0:
                self.energy = 0
            self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True