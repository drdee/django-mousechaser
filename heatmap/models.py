from django.db import models

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(verify_exists=False)
    width = models.IntegerField()
    height= models.IntegerField()
    
class HeatMap(models.Model):
    '''This model stores the mouse coordinates'''
    id = models.AutoField(primary_key=True)
    x_coord = models.TextField(blank=False, null=False)
    y_coord = models.TextField(blank=False, null=False)
    url = models.ForeignKey(Page)
    file = models.CharField(max_length=256)

class Element(models.Model):
    '''This model stores major html elements from a webpage
    currently it will search for div and p tags, see views.py'''    
    id = models.AutoField(primary_key=True)
    url = models.ForeignKey(Page)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    time_spent = models.IntegerField()