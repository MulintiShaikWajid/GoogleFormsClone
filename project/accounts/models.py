from django.db import models


class Person(models.Model):
    client_name = models.CharField(max_length=150)
    ans1 = models.CharField(max_length=120)
    ans2 = models.CharField(max_length=120)
    ans3 = models.CharField(max_length=120) 	

class Person2(models.Model):
	client_name = models.CharField(max_length=150)
	ans1 = models.CharField(max_length=120)
	ans2 = models.CharField(max_length=120)
	ans3 = models.CharField(max_length=120)    