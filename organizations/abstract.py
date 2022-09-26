# -*- coding: utf-8 -*-
import uuid
import warnings

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import six

from organizations.base import AbstractBaseInvitation
from organizations.base import AbstractBaseOrganization
from organizations.base import AbstractBaseOrganizationOwner
from organizations.base import AbstractBaseOrganizationUser
from organizations.base import OrgMeta
from organizations.fields import AutoCreatedField
from organizations.fields import AutoLastModifiedField
from organizations.fields import SlugField
from organizations.signals import owner_changed
from organizations.signals import user_added
from organizations.signals import user_removed

USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")
ORGS_TIMESTAMPED_MODEL = getattr(settings, "ORGS_TIMESTAMPED_MODEL", None)

if ORGS_TIMESTAMPED_MODEL:
    warnings.warn(
        "Configured TimestampModel has been replaced and is now ignored.",
        DeprecationWarning,
    )


class SharedBaseModel(models.Model):
    """
    Adds fields ``created`` and ``modified`` and
    two private methods that are used by the rest
    of the abstract models.
    """

    created = AutoCreatedField()
    modified = AutoLastModifiedField()

    @property
    def _org_user_model(self):
        model = self.__class__.module_registry[self.__class__.__module__][
            "OrgUserModel"
        ]
        if model is None:
            model = self.__class__.module_registry["organizations.models"][
                "OrgUserModel"
            ]
        return model

    @property
    def _org_owner_model(self):
        model = self.__class__.module_registry[self.__class__.__module__][
            "OrgOwnerModel"
        ]
        if model is None:
            model = self.__class__.module_registry["organizations.models"][
                "OrgOwnerModel"
            ]
        return model

    class Meta:
        abstract = True

class AbstractOrganizationJoin(models.Model):
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    company_name = models.CharField(max_length=200, default=None)
    company_number = models.IntegerField(default=None)
    company_website = models.URLField(default=None)
    company_industry = models.CharField(max_length=200, default=None)
    company_address = models.CharField(max_length=200, default=None)
    name = models.CharField(max_length=200, default=None)
    job_title = models.CharField(max_length=200, default=None)
    email = models.EmailField(default=None)
    email_verified = models.BooleanField(blank=True, null=True)
    contact_no = models.CharField(max_length=200, default=None)
    agree = models.BooleanField()
    #signature = JSignatureField()
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.uniqueId is None:
    #         self.uniqueId = 'B-'+ str(uuid.uuid4().int)[:4]
    #         self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
    #     #     self.model = Business.objects.create(company_name = self.company_name, company_number=self.company_number, full_name=self.name, email=self.email, phone=self.contact_no,
    #     #     job_title=self.job_title, unique_business=self, slug = slugify('{} {}'.format(self.company_name, self.uniqueId)))
    #     # self.slug = slugify('{} {}'.format(self.company_name, self.uniqueId))
    #
    #     super(AbstractOrganizationJoin, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name

    class Meta():
        abstract = True
        verbose_name = _("organization join")
        verbose_name_plural = _("organizations join")

# @receiver(post_save, sender=AbstractOrganizationJoin)
# def create_tabel(sender, instance, created, **kwargs):
#     if created:
#         AbstractBaseOrganization.objects.create(name=instance.company_name, company_number=instance.company_number,
#                                              full_name=instance.name, email=instance.email, phone=instance.contact_no,
#                                              job_title=instance.job_title, unique_business=instance,
#                                              slug=slugify('{} {}'.format(instance.company_name, instance.uniqueId)))

PAYMENT_TERM_CHOICES = [
    ('Weekly', 'Weekly'),
    ('Bi-Weekly', 'Bi-Weekly'),
    ('Monthly', 'Monthly'),
    ('Annually', 'Annually'),
    ('Quartely', 'Quartely'),
]
OUTPUT_PREFERENCE_CHOICES = [
    ('Email', 'Email'),
    ('Print', 'Print'),
    ('Email And Print', 'Email And Print'),
]

class AbstractOrganization(
    six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganization)
):
    """
    Abstract Organization model.
    """
    user_id = models.IntegerField(default=None, blank=True, null=True)
    company_number = models.IntegerField(default=None, blank=True, null=True)
    business_phone = models.CharField(max_length=200, default=None, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_address = models.CharField(max_length=200, default=None, blank=True, null=True)
    post_code = models.CharField(max_length=200, default=None, blank=True, null=True)
    city = models.CharField(max_length=200, default=None, blank=True, null=True)
    country = models.CharField(max_length=200, default=None, blank=True, null=True)
    industry = models.CharField(max_length=200, default=None, blank=True, null=True)
    # status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=None, blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)
    #LICENSING
    start_date = models.CharField(max_length=200, default=None, blank=True, null=True)
    # subscription_type = models.CharField(max_length=200, default=None)
    # subscription_expiry = models.DateField(auto_now=True)
    #INVOICING
    invoice_id = models.IntegerField(default=None, blank=True, null=True)
    payment_terms = models.CharField(max_length=200, choices=PAYMENT_TERM_CHOICES, default=None, blank=True, null=True)
    output_perference = models.CharField(max_length=200, choices=OUTPUT_PREFERENCE_CHOICES, default=None, blank=True, null=True)
    invoice_footer = models.CharField(max_length=200, default=None, blank=True, null=True)
    #DOCUMENTS
    registration_app_form = models.FileField(upload_to='registration_app_form/', default=None, blank=True, null=True)
    #REGISTERED PERSONAL DETAILS
    full_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    job_title = models.CharField(max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=200, default=None, blank=True, null=True)
    #PAYMENT DETAILS
    payment_card = models.CharField(max_length=200, default=None, blank=True, null=True)
    expiration = models.CharField(max_length=200, default=None, blank=True, null=True)
    #NOTES
    notes = models.TextField(blank=True, null=True)
    #PAYMENTS/VAT
    account_details_ref = models.CharField(max_length=200, default=None, blank=True, null=True)
    payment_on = models.CharField(max_length=200, default=None, blank=True, null=True)
    last_payment = models.CharField(max_length=200, default=None, blank=True, null=True)
    apply_vat = models.CharField(max_length=200, default=None, blank=True, null=True)
    vat_rate = models.CharField(max_length=200, default=None, blank=True, null=True)
    #CONTRACTUAL AGREEMENT
    contractual_agreement = models.FileField(upload_to='contractual_agreement/', default=None, blank=True, null=True)
    slug = SlugField(
        max_length=200,
        blank=False,
        editable=True,
        populate_from="name",
        unique=True,
        help_text=_("The name in all lowercase, suitable for URL identification"),
    )

    class Meta(AbstractBaseOrganization.Meta):
        abstract = True
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"organization_pk": self.pk})

    def add_user(self, user, is_admin=False):
        """
        Adds a new user and if the first user makes the user an admin and
        the owner.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True
        # TODO get specific org user?
        org_user = self._org_user_model.objects.create(
            user=user, organization=self, is_admin=is_admin
        )
        if users_count == 0:
            # TODO get specific org user?
            self._org_owner_model.objects.create(
                organization=self, organization_user=org_user
            )

        # User added signal
        user_added.send(sender=self, user=user)
        return org_user

    def remove_user(self, user):
        """
        Deletes a user from an organization.
        """
        org_user = self._org_user_model.objects.get(user=user, organization=self)
        org_user.delete()

        # User removed signal
        user_removed.send(sender=self, user=user)

    def get_or_add_user(self, user, **kwargs):
        """
        Adds a new user to the organization, and if it's the first user makes
        the user an admin and the owner. Uses the `get_or_create` method to
        create or return the existing user.

        `user` should be a user instance, e.g. `auth.User`.

        Returns the same tuple as the `get_or_create` method, the
        `OrganizationUser` and a boolean value indicating whether the
        OrganizationUser was created or not.
        """
        is_admin = kwargs.pop("is_admin", False)
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True

        org_user, created = self._org_user_model.objects.get_or_create(
            organization=self, user=user, defaults={"is_admin": is_admin}
        )
        if users_count == 0:
            self._org_owner_model.objects.create(
                organization=self, organization_user=org_user
            )
        if created:
            # User added signal
            user_added.send(sender=self, user=user)
        return org_user, created

    def change_owner(self, new_owner):
        """
        Changes ownership of an organization.
        """
        old_owner = self.owner.organization_user
        self.owner.organization_user = new_owner
        self.owner.save()

        # Owner changed signal
        owner_changed.send(sender=self, old=old_owner, new=new_owner)

    def is_admin(self, user):
        """
        Returns True is user is an admin in the organization, otherwise false
        """
        return (
            True if self.organization_users.filter(user=user, is_admin=True) else False
        )

    def is_owner(self, user):
        """
        Returns True is user is the organization's owner, otherwise false
        """
        return self.owner.organization_user.user == user


class AbstractOrganizationUser(
    six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganizationUser)
):
    """
    Abstract OrganizationUser model
    """

    is_admin = models.BooleanField(default=False)

    class Meta(AbstractBaseOrganizationUser.Meta):
        abstract = True
        verbose_name = _("organization user")
        verbose_name_plural = _("organization users")

    def __str__(self):
        return "{0} ({1})".format(
            self.name if self.user.is_active else self.user.email,
            self.organization.name,
        )

    def delete(self, using=None):
        """
        If the organization user is also the owner, this should not be deleted
        unless it's part of a cascade from the Organization.

        If there is no owner then the deletion should proceed.
        """
        from organizations.exceptions import OwnershipRequired

        try:
            if self.organization.owner.organization_user.pk == self.pk:
                raise OwnershipRequired(
                    _(
                        "Cannot delete organization owner "
                        "before organization or transferring ownership."
                    )
                )
        # TODO This line presumes that OrgOwner model can't be modified
        except self._org_owner_model.DoesNotExist:
            pass
        super().delete(using=using)

    def get_absolute_url(self):
        return reverse(
            "organization_user_detail",
            kwargs={"organization_pk": self.organization.pk, "user_pk": self.user.pk},
        )


class AbstractOrganizationOwner(
    six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseOrganizationOwner)
):
    """
    Abstract OrganizationOwner model
    """

    class Meta:
        abstract = True
        verbose_name = _("organization owner")
        verbose_name_plural = _("organization owners")

    def save(self, *args, **kwargs):
        """
        Extends the default save method by verifying that the chosen
        organization user is associated with the organization.

        Method validates against the primary key of the organization because
        when validating an inherited model it may be checking an instance of
        `Organization` against an instance of `CustomOrganization`. Mutli-table
        inheritance means the database keys will be identical though.

        """
        from organizations.exceptions import OrganizationMismatch

        if self.organization_user.organization.pk != self.organization.pk:
            raise OrganizationMismatch
        else:
            super().save(*args, **kwargs)


class AbstractOrganizationInvitation(
    six.with_metaclass(OrgMeta, SharedBaseModel, AbstractBaseInvitation)
):
    """
    Abstract OrganizationInvitationBase model
    """

    class Meta:
        abstract = True
