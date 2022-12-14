# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify
from django.utils.translation import gettext_lazy as _

from organizations.abstract import AbstractOrganization, AbstractOrganizationJoin
from organizations.abstract import AbstractOrganizationInvitation
from organizations.abstract import AbstractOrganizationOwner
from organizations.abstract import AbstractOrganizationUser


class OrganizationJoin(AbstractOrganizationJoin):
    """
    Default Organization Join model.
    """
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = 'B-'+ str(uuid.uuid4().int)[:4]
            self.slug = slugify('{}'.format(self.company_name))
        #     self.model = Business.objects.create(company_name = self.company_name, company_number=self.company_number, full_name=self.name, email=self.email, phone=self.contact_no,
        #     job_title=self.job_title, unique_business=self, slug = slugify('{} {}'.format(self.company_name, self.uniqueId)))
        # self.slug = slugify('{} {}'.format(self.company_name, self.uniqueId))

        super(OrganizationJoin, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name

    class Meta():
        abstract = False

@receiver(post_save, sender=OrganizationJoin)
def create_tabel(sender, instance, created, **kwargs):
    if created:
        Organization.objects.create(name=instance.company_name, company_number=instance.company_number,
                                             full_name=instance.name, email=instance.email, phone=instance.contact_no,
                                             job_title=instance.job_title, unique_business=instance,
                                             slug=slugify('{}'.format(instance.company_name))
                                    )


class Organization(AbstractOrganization):
    unique_business = models.ForeignKey(OrganizationJoin, on_delete=models.CASCADE, max_length=100, default=None, blank=True, null=True)
    """
    Default Organization model.
    """

    def TotalMemberCount(self):
        trancount = OrganizationUser.objects.filter(user__is_active=True, organization=self).count()
        return trancount

    def PendingMemberCount(self):
        trancount = OrganizationUser.objects.filter(user__is_active=False, organization=self).count()
        return trancount

    class Meta(AbstractOrganization.Meta):
        abstract = False


class OrganizationUser(AbstractOrganizationUser):
    """
    Default OrganizationUser model.
    """

    class Meta(AbstractOrganizationUser.Meta):
        abstract = False


class OrganizationOwner(AbstractOrganizationOwner):
    """
    Default OrganizationOwner model.
    """

    class Meta(AbstractOrganizationOwner.Meta):
        abstract = False


class OrganizationInvitation(AbstractOrganizationInvitation):
    class Meta(AbstractOrganizationInvitation.Meta):
        abstract = False
