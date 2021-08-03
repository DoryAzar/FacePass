from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_on", "updated_on")


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner",  "is_active",
                    "created_on", "updated_on")
    filter_horizontal = ["requested_information"]


class PassAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "company", "is_active",
                    "created_on", "updated_on")
    filter_horizontal = ["allowed_information"]


class AllowedInformationAdmin(admin.ModelAdmin):
    list_display = ["id", "field", "created_on", "updated_on"]


class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "firstname",
                    "lastname", "created_on", "updated_on")


# Registered models
admin.site.register(User, UserAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(Pass, PassAdmin)
admin.site.register(AllowedInformation, AllowedInformationAdmin)
admin.site.register(PersonalInformation, PersonalInformationAdmin)
