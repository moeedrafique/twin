# Generated by Django 3.2.10 on 2022-09-16 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_auto_20220916_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='unique_business',
            field=models.ForeignKey(blank=True, default=None, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organizationjoin'),
        ),
    ]
