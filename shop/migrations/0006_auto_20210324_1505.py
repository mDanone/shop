# Generated by Django 3.1.7 on 2021-03-24 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_userprofile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
    ]