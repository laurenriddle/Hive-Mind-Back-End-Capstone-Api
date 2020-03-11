
from django.db import models
from django.contrib.auth.models
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE

class Cohort(SafeDeleteModel):
    """
    This makes an cohort instance and defines the columns in the DB
   
    NOTE: This model imports the Django SafeDeleteModel
    """

        _safedelete_policy = HARD_DELETE_NOCASCADE


    cohort = models.CharField(max_length=75, null=True)
    

    class Meta:
        verbose_name = ("cohort")
        verbose_name_plural = ("cohorts")
    def __str__(self):
        return f'{self.cohort}'