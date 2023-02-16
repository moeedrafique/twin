# -*- coding: utf-8 -*-

from django.contrib import admin
# from organizations.models import OrganizationJoin, Floors, Building
from organizations import models
from organizations.base_admin import BaseOrganizationAdmin
from organizations.base_admin import BaseOrganizationOwnerAdmin
from organizations.base_admin import BaseOrganizationUserAdmin
from organizations.base_admin import BaseOwnerInline


# admin.site.register(OrganizationJoin)
# admin.site.register(Building)
# admin.site.register(Floors)

class OwnerInline(BaseOwnerInline):
    model = models.OrganizationOwner


@admin.register(models.Organization)
class OrganizationAdmin(BaseOrganizationAdmin):
    inlines = [OwnerInline]


@admin.register(models.OrganizationUser)
class OrganizationUserAdmin(BaseOrganizationUserAdmin):
    pass


@admin.register(models.OrganizationOwner)
class OrganizationOwnerAdmin(BaseOrganizationOwnerAdmin):
    pass


@admin.register(models.OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    pass


