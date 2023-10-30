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

class SpiderHero(Hero, RechargeEnergyMixin):
    SPIDER_HERO_ENERGY_DECREASE = 80

    def swing_from_buildings(self):
        if self.energy <= 0:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        else:
            self.energy -= self.SPIDER_HERO_ENERGY_DECREASE
            return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True

class FlashHero(Hero, RechargeEnergyMixin):
    FLASH_HERO_ENERGY_DECREASE = 65

    def run_at_super_speed(self):
        if self.energy <= 0:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        else:
            self.energy -= self.FLASH_HERO_ENERGY_DECREASE
            self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True
