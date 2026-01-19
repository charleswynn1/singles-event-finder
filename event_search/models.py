from django.db import models
import datetime
'''
class Event(models.Model):
    event_name = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    venue = models.CharField(blank = True)
    city = models.CharField(max_length = 30)
    state = models.CharField(max_length = 30)
    country = models.CharField(max_length = 30)
    date_and_time = models.DateField(default = datetime.date.today)
    create_date = models.DateField(auto_now_add=True)
    url = models.URLField(blank = True)   
    
    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ['date_and_time']

'''

# Create your models here.
