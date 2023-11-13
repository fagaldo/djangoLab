from django.db import models

# Create your models here.
class Cars(models.Model):
    model = models.CharField(max_length = 25)
    brand = models.CharField(max_length = 25)
    year = models.IntegerField()
    create_time = models.DateTimeField('create time')
    last_edit_time = models.DateTimeField('last edit time')
