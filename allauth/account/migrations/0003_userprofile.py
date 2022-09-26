# Generated by Django 3.2.10 on 2022-09-16 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_email_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.FileField(default='staff-user/', upload_to='staff-pictures')),
                ('dob', models.CharField(default=None, max_length=255)),
                ('id_card_no', models.CharField(default=None, max_length=255)),
                ('city', models.CharField(default=None, max_length=255, null=True)),
                ('postal_code', models.CharField(default=None, max_length=255, null=True)),
                ('house_address', models.CharField(default=None, max_length=255)),
                ('phone_number', models.CharField(default=None, max_length=255)),
                ('landline', models.CharField(default=None, max_length=255, null=True)),
                ('emergency_contact', models.CharField(default=None, max_length=255)),
                ('medical_history', models.CharField(default=None, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auth_user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
