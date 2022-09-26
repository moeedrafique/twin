from django.contrib import admin
from main_app import models
from main_app.base_admin import BaseOrganizationAdmin
from main_app.base_admin import BaseOrganizationOwnerAdmin
from main_app.base_admin import BaseOrganizationUserAdmin
from main_app.base_admin import BaseOwnerInline

# Register your models here.
#
# admin.site.register(Organization)

class OwnerInline(BaseOwnerInline):
    model = models.OrganizationOwner


@admin.register(models.Organization)
class OrganizationAdmin(BaseOrganizationAdmin):
    pass
    # inlines = [OwnerInline]

# #
@admin.register(models.OrganizationUser)
class OrganizationUserAdmin(BaseOrganizationUserAdmin):
    pass


@admin.register(models.OrganizationOwner)
class OrganizationOwnerAdmin(BaseOrganizationOwnerAdmin):
    pass