from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    admins = models.ManyToManyField("User", related_name="admin", blank=True, null=True)

    def __str__(self):
        return self.name


class JoinRequest(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    emails = models.JSONField(default=list)
    users = models.ManyToManyField(
        "User", related_name="join_request", blank=True, null=True
    )
    is_admin_access = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.organization}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["organization"]

    def __str__(self):
        return self.email
