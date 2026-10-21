from django.db import models
import uuid

class Consulting(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('COMPLETED', 'Terminé'),
        ('CANCELLED', 'Annulé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200, default="Diagnostic juridique")
    
    full_name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=50, blank=True, default="")

    email = models.EmailField()

    description = models.TextField()

    meet_day = models.DateField()

    consulting_hour = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "rendez-vous pour consultance"
        verbose_name_plural = "rendez-vous pour consultance"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['meet_day', 'consulting_hour'],
                name='unique_creneau'
            )
        ]

    def __str__(self):
        return f"Rendez-vous pris par {self.full_name} pour le {self.meet_day} à {self.consulting_hour}"