from django.db import models
from django.utils.timezone import now

class DailyVisit(models.Model):
    date = models.DateField(default=now)
    country = models.CharField(max_length=100, default='Inconnu')
    visits = models.PositiveIntegerField(default=0)

    class Meta:
        # On agrège les visites par jour ET par pays pour éviter les doublons
        unique_together = ('date', 'country')
        verbose_name = "Visite journalière"
        verbose_name_plural = "Visites journalières"

    def __str__(self):
        return f"{self.date} - {self.country} : {self.visits} visites"