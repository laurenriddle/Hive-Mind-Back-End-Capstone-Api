
from django.db import models
from django.contrib.auth.models

class Industry(models.Model):
    """
    This makes an industry instance and defines the columns in the DB
   
   
    """



    industry = models.CharField(max_length=75, null=True)
    

    class Meta:
        verbose_name = ("industry")
        verbose_name_plural = ("industries")
    def __str__(self):
        return f'{self.industry}'