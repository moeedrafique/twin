from django.urls import reverse

from main_app.base import *
from django.utils.translation import gettext_lazy as _
from django.db import models
from main_app.fields import SlugField, AutoCreatedField, AutoLastModifiedField


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

class AbstractOrganization(SharedBaseModel, AbstractBaseOrganization):
    """
    Abstract Organization model.
    """
    company_number = models.IntegerField(default=None, blank=True, null=True)
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


class AbstractOrganizationUser(AbstractBaseOrganizationUser):
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

class AbstractOrganizationOwner(AbstractBaseOrganizationOwner):
    """
    Abstract OrganizationOwner model
    """

    class Meta:
        abstract = True
        verbose_name = _("organization owner")
        verbose_name_plural = _("organization owners")