import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from jsignature.fields import JSignatureField
from uuid import uuid4
from django.utils.text import slugify
from django.db.models.signals import post_save
# Create your models here.
from main_app.abstract import *


class Organization(AbstractOrganization):
    """
    Default Organization model.
    """

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
# class User_Profile(models.Model):
#     user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=200, default=None)
#     last_name = models.CharField(max_length=200, default=None)
#
#
# class Join(models.Model):
#     uniqueId = models.CharField(null=True, blank=True, max_length=100)
#     company_name = models.CharField(max_length=200, default=None)
#     company_number = models.IntegerField(default=None)
#     company_website = models.URLField(default=None)
#     company_industry = models.CharField(max_length=200, default=None)
#     company_address = models.CharField(max_length=200, default=None)
#     name = models.CharField(max_length=200, default=None)
#     job_title = models.CharField(max_length=200, default=None)
#     email = models.EmailField(default=None)
#     email_verified = models.BooleanField(blank=True, null=True)
#     contact_no = models.CharField(max_length=200, default=None)
#     agree = models.BooleanField()
#     #signature = JSignatureField()
#     slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
#
#     def save(self, *args, **kwargs):
#         if self.uniqueId is None:
#             self.uniqueId = 'B-'+ str(uuid.uuid4().int)[:4]
#             self.slug = slugify('{} {}'.format(self.company_name, self.uniqueId))
#         #     self.model = Business.objects.create(company_name = self.company_name, company_number=self.company_number, full_name=self.name, email=self.email, phone=self.contact_no,
#         #     job_title=self.job_title, unique_business=self, slug = slugify('{} {}'.format(self.company_name, self.uniqueId)))
#         # self.slug = slugify('{} {}'.format(self.company_name, self.uniqueId))
#
#         super(Join, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.company_name
#
# @receiver(post_save, sender=Join)
# def create_tabel(sender, instance, created, **kwargs):
#     if created:
#         Business.objects.create(company_name=instance.company_name, company_number=instance.company_number,
#                                              full_name=instance.name, email=instance.email, phone=instance.contact_no,
#                                              job_title=instance.job_title, unique_business=instance,
#                                              slug=slugify('{} {}'.format(instance.company_name, instance.uniqueId)))
# STATUS_CHOICES = [
#     ('Active', 'Active'),
#     ('Deactive', 'Deactive'),
# ]
# PAYMENT_TERM_CHOICES = [
#     ('Weekly', 'Weekly'),
#     ('Bi-Weekly', 'Bi-Weekly'),
#     ('Monthly', 'Monthly'),
#     ('Annually', 'Annually'),
#     ('Quartely', 'Quartely'),
# ]
# OUTPUT_PREFERENCE_CHOICES = [
#     ('Email', 'Email'),
#     ('Print', 'Print'),
#     ('Email And Print', 'Email And Print'),
# ]
# class Business(models.Model):
#     unique_business = models.ForeignKey(Join, on_delete=models.CASCADE, max_length=100, default=None, blank=True, null=True)
#     user_id = models.IntegerField(default=None, blank=True, null=True)
#     ref_id = models.IntegerField(default=None, blank=True, null=True)
#     company_name = models.CharField(max_length=200, default=None, blank=True, null=True)
#     company_number = models.IntegerField(default=None, blank=True, null=True)
#     business_phone = models.CharField(max_length=200, default=None, blank=True, null=True)
#     business_email = models.EmailField(blank=True, null=True)
#     business_address = models.CharField(max_length=200, default=None, blank=True, null=True)
#     post_code = models.CharField(max_length=200, default=None, blank=True, null=True)
#     city = models.CharField(max_length=200, default=None, blank=True, null=True)
#     country = models.CharField(max_length=200, default=None, blank=True, null=True)
#     industry = models.CharField(max_length=200, default=None, blank=True, null=True)
#     status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=None, blank=True, null=True)
#     last_active = models.DateTimeField(auto_now=True)
#     #LICENSING
#     start_date = models.CharField(max_length=200, default=None, blank=True, null=True)
#     # subscription_type = models.CharField(max_length=200, default=None)
#     # subscription_expiry = models.DateField(auto_now=True)
#     #INVOICING
#     invoice_id = models.IntegerField(default=None, blank=True, null=True)
#     payment_terms = models.CharField(max_length=200, choices=PAYMENT_TERM_CHOICES, default=None, blank=True, null=True)
#     output_perference = models.CharField(max_length=200, choices=OUTPUT_PREFERENCE_CHOICES, default=None, blank=True, null=True)
#     invoice_footer = models.CharField(max_length=200, default=None, blank=True, null=True)
#     #DOCUMENTS
#     registration_app_form = models.FileField(upload_to='registration_app_form/', default=None, blank=True, null=True)
#     #REGISTERED PERSONAL DETAILS
#     full_name = models.CharField(max_length=200, default=None, blank=True, null=True)
#     job_title = models.CharField(max_length=200, default=None, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     phone = models.CharField(max_length=200, default=None, blank=True, null=True)
#     #PAYMENT DETAILS
#     payment_card = models.CharField(max_length=200, default=None, blank=True, null=True)
#     expiration = models.CharField(max_length=200, default=None, blank=True, null=True)
#     #NOTES
#     notes = models.TextField(blank=True, null=True)
#     #PAYMENTS/VAT
#     account_details_ref = models.CharField(max_length=200, default=None, blank=True, null=True)
#     payment_on = models.CharField(max_length=200, default=None, blank=True, null=True)
#     last_payment = models.CharField(max_length=200, default=None, blank=True, null=True)
#     apply_vat = models.CharField(max_length=200, default=None, blank=True, null=True)
#     vat_rate = models.CharField(max_length=200, default=None, blank=True, null=True)
#     #CONTRACTUAL AGREEMENT
#     contractual_agreement = models.FileField(upload_to='contractual_agreement/', default=None, blank=True, null=True)
#     # slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
#     # IMG TYPE
#     filename_type1 = models.CharField(max_length=200, default=None, blank=True, null=True)
#     filename_type2 = models.CharField(max_length=200, default=None, blank=True, null=True)
#
#     def __str__(self):
#         return self.company_name
#
#
#
#
#
#
#

















