from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta():
        verbose_name_plural = "Income"

    def __str__(self):
        return '%s -- %s -- %s' % (self.owner, self.amount, self.date)
