# Generated by Django 3.2.4 on 2022-03-06 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0009_comment_file_member_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='type',
            field=models.CharField(default=2, max_length=10),
            preserve_default=False,
        ),
    ]