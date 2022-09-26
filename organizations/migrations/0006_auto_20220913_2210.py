# Generated by Django 3.2.10 on 2022-09-13 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_organization_company_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='account_details_ref',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='apply_vat',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='business_address',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='business_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='business_phone',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='city',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='contractual_agreement',
            field=models.FileField(blank=True, default=None, null=True, upload_to='contractual_agreement/'),
        ),
        migrations.AddField(
            model_name='organization',
            name='country',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='expiration',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='full_name',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='industry',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='invoice_footer',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='invoice_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='job_title',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_active',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_payment',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='output_perference',
            field=models.CharField(blank=True, choices=[('Email', 'Email'), ('Print', 'Print'), ('Email And Print', 'Email And Print')], default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='payment_card',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='payment_on',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='payment_terms',
            field=models.CharField(blank=True, choices=[('Weekly', 'Weekly'), ('Bi-Weekly', 'Bi-Weekly'), ('Monthly', 'Monthly'), ('Annually', 'Annually'), ('Quartely', 'Quartely')], default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='post_code',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='registration_app_form',
            field=models.FileField(blank=True, default=None, null=True, upload_to='registration_app_form/'),
        ),
        migrations.AddField(
            model_name='organization',
            name='start_date',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='vat_rate',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]