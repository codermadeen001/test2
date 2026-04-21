from django.db import models
from django.conf import settings
from django.utils import timezone


class Field(models.Model):
    CROP_CHOICES = [
        ('Corn', 'Corn'),
        ('Wheat', 'Wheat'),
        ('Soybeans', 'Soybeans'),
        ('Rice', 'Rice'),
        ('Barley', 'Barley'),
        ('Other', 'Other'),
    ]

    STAGE_CHOICES = [
        ('Planted', 'Planted'),
        ('Growing', 'Growing'),
        ('Ready', 'Ready'),
        ('Harvested', 'Harvested'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    crop_type = models.CharField(max_length=50, choices=CROP_CHOICES)

    # Automatically set when record is created
    planting_date = models.DateField(auto_now_add=True)

    current_stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='Planted'
    )

    old_stage= models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='Planted'
    )

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_fields'
    )
    notes = models.TextField(blank=True)
    updated_at=models.DateTimeField(auto_now=True)

    created_by_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_fields'
    )

    created_at = models.DateTimeField(default=timezone.now)

    # ---------------------------
    # BUSINESS LOGIC
    # ---------------------------
    def calculate_status(self):
        """
        Determine farm risk status based on crop stage and time since planting
        """
        today = timezone.localdate()
        days_since_planting = (today - self.planting_date).days

        # Completed case
        if self.current_stage == 'Harvested':
            return 'Completed'

        # Risk thresholds 
        thresholds = {
            'Planted': 30,
            'Growing': 60,
            'Ready': 90,
        }

        # At Risk logic
        if self.current_stage in thresholds:
            if days_since_planting > thresholds[self.current_stage]:
                return 'At Risk'

        return 'Active'

    # ---------------------------
    # PROPERTY 
    # ---------------------------
    @property
    def status(self):
        return self.calculate_status()

    def __str__(self):
        return f"{self.name} - {self.crop_type}"

    class Meta:
        db_table = 'fields'