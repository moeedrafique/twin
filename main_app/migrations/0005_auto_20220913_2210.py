# Generated by Django 3.2.10 on 2022-09-13 17:10

from django.db import migrations
import django.utils.timezone
import main_app.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_organizationowner_organizationuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created',
            field=main_app.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='modified',
            field=main_app.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organizationowner',
            name='created',
            field=main_app.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organizationowner',
            name='modified',
            field=main_app.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organizationuser',
            name='created',
            field=main_app.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organizationuser',
            name='modified',
            field=main_app.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False),
        ),
    ]