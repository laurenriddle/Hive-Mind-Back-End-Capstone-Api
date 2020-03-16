from django.db import models
from .Applicant import Applicant
from .Company import Company
class Interview(models.Model):
    """
    This makes an interview instance and defines the columns in the DB
   
    Foreign keys: applicant_id and company_id
    
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    offer = models.BooleanField()
    position = models.CharField(max_length=200, null=True)
    date = models.DateField(max_length=200, null=True)
    review = models.CharField(max_length=7000, null=True)
    advice = models.CharField(max_length=7000, null=True)
    interview_type = models.CharField(max_length=300, null=True)
    in_person = models.BooleanField()
    code_challege = models.BooleanField()
    

    class Meta:
        verbose_name = ("interview")
        verbose_name_plural = ("interviews")
    def __str__(self):
        return f'{self.review} {self.advice}'