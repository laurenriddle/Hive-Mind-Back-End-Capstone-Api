from django.db import models
from django.contrib.auth.models import User
from .Cohort import Cohort

class Applicant(models.Model):
    """
    This makes an applicant instance and defines the columns in the DB
    Foreign keys: user_id and cohort_id

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    is_employed = models.BooleanField()
    linkedin_profile = models.CharField(max_length=500, null=True)
    image = models.CharField(max_length=300, null=True)
    employer = models.CharField(max_length=300, null=True)
    aboutme = models.CharField(max_length=1000, null=True)
    jobtitle = models.CharField(max_length=300, null=True)
    location = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = ("applicant")
        verbose_name_plural = ("applicants")
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'