# Generated by Django 3.2.4 on 2022-03-09 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0031_auto_20220309_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='auto_add',
            field=models.BooleanField(default=True),
        ),
    ]
