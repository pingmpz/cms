# Generated by Django 3.2.4 on 2022-05-09 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0059_auto_20220506_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Costing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
            ],
        ),
    ]