from django.db import models
import random
from django.urls import reverse
from django.utils import timezone
import time
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    thumb = models.ImageField()


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)
    history = models.TextField(max_length=1000, null=True, blank=True, default='No History')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("emsi:dept_detail", kwargs={"pk": self.pk})


class Employee(models.Model):
    LANGUAGE = (('english', 'ENGLISH'), ('arabic', 'ARABIC'), ('french', 'FRENCH'))
    GENDER = (('male', 'MALE'), ('female', 'FEMALE'))
    emp_id = models.CharField(max_length=70, default='emp' + str(random.randrange(100, 999, 1)))
    thumb = models.ImageField(blank=True, null=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=125, null=False)
    address = models.TextField(max_length=100, default='')
    emergency = models.CharField(max_length=11)
    gender = models.CharField(choices=GENDER, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    joined = models.DateTimeField(default=timezone.now)
    language = models.CharField(choices=LANGUAGE, max_length=10, default='english')
    nuban = models.CharField(max_length=10, default='0123456789')
    bank = models.CharField(max_length=25, default='First Bank Plc')
    salary = models.CharField(max_length=16, default='00,000.00')

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("emsi:employee_view", kwargs={"pk": self.pk})
