from django.db import models
import uuid

# Create your models here.
class Consulting(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    
    full_name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    description = models.TextField()

    meet_day = models.DateField()

    consulting_hour = models.TimeField()

    # Timestamp

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
        return f"rendez-vous pris par {self.full_name} pour le {self.meet_day}"


    