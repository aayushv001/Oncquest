from django.db import models
from django.utils.translation import gettext_lazy as lazy
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,name,username,password,role,**other_fields):

        if not username:
            raise ValueError(lazy('you must provide username'))
        if not password:
            raise ValueError(lazy('you must provide password'))
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        user=self.model(name=name,username=username,role=role,**other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,name,username,password,role,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        return self.create_user(name,username,password,role,**other_fields)
class data(AbstractBaseUser,PermissionsMixin):
    name=models.TextField()
    username=models.CharField(max_length=100, unique=True)
    password=models.TextField()
    role=models.CharField(max_length=20)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects=AccountManager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['password','role','name']

    def ___str___(self):
        return self.username
class pdata(models.Model):
    srfid=models.TextField(unique=True)
    bcode=models.TextField()
    pname=models.TextField()
    mobno=models.TextField()
    age=models.TextField()
    gender=models.TextField()
    address=models.TextField()
    ccode=models.TextField()
    dname=models.TextField()
    rem=models.TextField()
    cexe=models.TextField()
    email=models.EmailField()
    loc=models.TextField()
    runid=models.TextField()
    runtime=models.TextField()
    icmrup=models.TextField()
    accid=models.TextField()
    res=models.TextField()
    ctval=models.TextField() 
    runstat=models.CharField(max_length=2) 
class regdata(models.Model):
    srfid=models.TextField(unique=True)
    pname=models.TextField()
    mobno=models.TextField()
    age=models.TextField()
    gender=models.TextField()
    address=models.TextField()
    ccode=models.TextField()
    dname=models.TextField()
    rem=models.TextField()
    cexe=models.TextField()
    email=models.TextField()       


