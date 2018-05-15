from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
	name = models.CharField(max_length=200)
	maker = models.ForeignKey(User,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name

class Topping(models.Model):
	pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name
