from django.db import models
from .Industry import Industry

class Company(models.Model):
    """
    This makes an company instance and defines the columns in the DB
    Foreign keys: industry_id

    """

    name = models.CharField(max_length=75, null=True)
    city = models.CharField(max_length=75, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("company")
        verbose_name_plural = ("companies")
    def __str__(self):
        return f'{self.name}'