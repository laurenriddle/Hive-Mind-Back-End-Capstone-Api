from django.db import models
from .Applicant import Applicant
class Friend(models.Model):
    """
    This makes an interview instance and defines the columns in the DB
   
    Foreign keys: applicant_id and company_id
    
    """
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    friend = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='friends')

    class Meta:
        verbose_name = ("friend")
        verbose_name_plural = ("friends")
    def __str__(self):
        return f'{self.applicant}'