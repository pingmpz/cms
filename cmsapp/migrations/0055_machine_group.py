# Generated by Django 3.2.4 on 2022-04-02 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0054_sectiongroup_line_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='group',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
