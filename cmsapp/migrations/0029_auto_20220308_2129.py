# Generated by Django 3.2.4 on 2022-03-08 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0028_auto_20220308_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='scheme',
            field=models.CharField(default='Light Mode', max_length=10),
        ),
        migrations.AddField(
            model_name='employee',
            name='sidebar',
            field=models.CharField(default='Scrollable', max_length=10),
        ),
    ]