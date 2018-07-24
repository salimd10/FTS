from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name


class File(models.Model):
    file_id = models.CharField(max_length=200)
    name = models.CharField(max_length=400)

    # status = models.CharField(max_length=30,default='')
    # location = models.CharField(max_length=30,default='')
    # destination = models.CharField(max_length=30, default='')
    # origin = models.ForeignKey(Office, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name

class FileTracker(models.Model):
    file_id = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=400, default='')
    sender = models.CharField(max_length=30, default='', null=True,blank=True)
    receiver = models.CharField(max_length=30, default='', null=True,blank=True)
    status = models.CharField(max_length=30, default='', null=True,blank=True)

    # status = models.CharField(max_length=30,default='')
    # location = models.CharField(max_length=30,default='')
    # destination = models.CharField(max_length=30, default='')
    # origin = models.ForeignKey(Office, on_delete=modeleciver = models.charfield(max_length=30, default='')
    objects = models.Manager()

    def __str__(self):
        return self.name

class FilesLogs(models.Model):
    file_id = models.CharField(max_length=200)
    name = models.CharField(max_length=400)
    sender = models.CharField(max_length=30, default='', null=True,blank=True)
    receiver = models.CharField(max_length=30, default='', null=True,blank=True)
    status = models.CharField(max_length=30, default='', null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Staff(models.Model):
    staff_id = models.CharField(unique=True, max_length=8)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    admin_status = models.BooleanField(default=False)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    # phone = models.CharField(max_length=11)
    # email = models.EmailField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.first_name + ' ' + self.surname


class StaffLogin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=20, default="password")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.username
