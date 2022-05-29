from django.db import models

# Create your models here.
class UserName(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return "pk {} : {}".format(self.pk,self.name)
