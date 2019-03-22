from django.db import models

# Create your models here.


class Users(models.Model):
    Nick = models.CharField(max_length=20, unique=True, default='')
    Psd = models.CharField(max_length=100)
    UserId = models.AutoField(primary_key=True)


class Articles(models.Model):
    Tag = models.CharField(max_length=20, null=False)
    Title = models.CharField(max_length=20, primary_key=True)
    Bode = models.TextField(default='')
    UserId = models.ForeignKey(Users, on_delete=models.CASCADE)
    CreateTime = models.DateTimeField(auto_now_add=True)
    UpdateTime = models.CharField(max_length=50, default='')


class UserTags(models.Model):
    UserId = models.ForeignKey(Users, on_delete=models.CASCADE)
    Tags = models.CharField(max_length=20)

