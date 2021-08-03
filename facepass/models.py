import inspect
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import utils


class Information(models.TextChoices):
    """
    Personal Information that can be controller
    by a user

    """
    FIRSTNAME = "firstname"
    LASTNAME = "lastname"
    EMAIL = "email"
    BIRTHDATE = "birthdate"
    AGE = "age"
    ADDRESS = "address"
    CITY = "city"
    COUNTRY = "country"
    POSTAL_CODE = "postal_code"
    SSN = "ssn"
    PHONE_NUMBER = "phone_number"
    CREDIT_CARD_NUMBER = "credit_card_number"

    # method that returns the properties out of the model
    def get_information(self, labels=False):
        return [choice[labels] for choice in Information.choices]


class User(AbstractUser):
    """
    User Model

    """
    face_signature = models.JSONField(blank=True, default=str)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }

    def signature(self):
        return {
            "id": self.id,
            "username": self.username,
            "label": f"{self.id}",
            "images": self.face_signature
        }


class PersonalInformation(models.Model):

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="personal_information",
        blank=True, null=True, default=None)
    firstname = models.CharField(
        max_length=50, blank=True, null=True,  default=None)
    lastname = models.CharField(
        max_length=50, blank=True, null=True,  default=None)
    email = models.EmailField(blank=True, null=True,  default=None)
    birthdate = models.DateTimeField(blank=True, null=True, default=None)
    age = models.IntegerField(blank=True, null=True, default=None)
    address = models.CharField(
        max_length=200, blank=True, null=True, default=None)
    city = models.CharField(max_length=200, blank=True,
                            null=True, default=None)
    country = models.CharField(
        max_length=200, blank=True, null=True, default=None)
    postal_code = models.CharField(
        max_length=10, blank=True, null=True, default=None)
    ssn = models.CharField(max_length=16, blank=True, null=True, default=None)
    phone_number = models.CharField(
        validators=[utils.validate_phone],
        max_length=17, blank=True, null=True, default=None)
    credit_card_number = models.CharField(
        max_length=16, blank=True, null=True, default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}"

    def serialize(self):
        return {
            "owner": self.owner.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "birthdate": self.birthdate,
            "age": self.age,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "ssn": self.ssn,
            "phone_number": self.phone_number,
            "credit_card_number": self.credit_card_number
        }


class CompanyProfile(models.Model):
    """
    Company Profile

    """
    name = models.CharField(max_length=200)
    api_key = models.CharField(
        max_length=30, blank=True, null=True, default=None, unique=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_profiles")
    requested_information = models.ManyToManyField(
        "AllowedInformation", related_name="company_profiles",
        blank=True, default=None)
    success_url = models.URLField(blank=True, null=True, default=None)
    error_url = models.URLField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_requested_information(self):
        return [information.field
                for information
                in self.requested_information.all()]

    def serialize(self):
        return {
            "name": self.name,
            "api_key": self.api_key,
            "owner": self.owner.username,
            "requested_information":
                [
                    information.serialize()
                    for information
                    in self.requested_information.all()
                ],
            "success_url": self.success_url,
            "error_url": self.error_url,
            "is_active": self.is_active
        }


class Pass(models.Model):
    """
    Pass

    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="passes")

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                related_name="passes")

    is_restricted = models.BooleanField(default=False)

    allowed_information = models.ManyToManyField(
        "AllowedInformation", related_name="passes", blank=True, default=None)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Passes"

    def __str__(self):
        return f"{self.owner}-{self.company.name}"

    def get_allowed_information(self):
        return [
            information.field
            for information
            in self.allowed_information.all()
        ]

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "company_id": self.company.id,
            "company": self.company.name,
            "is_restricted": self.is_restricted,
            "allowed_information": [
                information.field
                for information
                in self.allowed_information.all()
            ],
            "is_active": self.is_active,
        }


class AllowedInformation(models.Model):
    """
    Allowed Information

    """

    field = models.CharField(
        max_length=200, choices=Information.choices, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field}"

    def serialize(self):
        return {
            "field": self.field
        }
