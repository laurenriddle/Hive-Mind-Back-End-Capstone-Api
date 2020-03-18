from django.db import models
from .Applicant import Applicant
from .Interview import Interview

class Favorite(models.Model):
    """
    This makes an favorite instance and defines the columns in the DB
    Foreign keys: interview_id, applicant_id

    """

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("favorite")
        verbose_name_plural = ("favorites")
        
    def __str__(self):
        return f'{self.applicant.user.first_name}'