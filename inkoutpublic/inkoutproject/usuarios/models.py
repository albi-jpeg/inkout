from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now


# Create your models here.



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type='usuario', **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, user_type='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')

        return self.create_user(email, password, user_type='admin', **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        ('usuario', 'Usuario'),
        ('artista', 'Artista'),
        ('admin', 'Administrador'),
    )

    username = None
    nombre = models.CharField(max_length=20, null=True)
    foto_perfil = models.ImageField(verbose_name='Foto_perfil', null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='usuario')
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']  

    objects = MyUserManager()

    def __str__(self):
        return self.email
        
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False
    
    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False
    