# Generated by Django 3.2.4 on 2022-09-07 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CriticalPart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('mat_code', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('minimum', models.IntegerField(default=0)),
                ('note', models.TextField(max_length=1000, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('mc_no', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('section', models.CharField(max_length=50, null=True)),
                ('register_no', models.CharField(max_length=50, null=True)),
                ('asset_no', models.CharField(max_length=50, null=True)),
                ('serial_no', models.CharField(max_length=50, null=True)),
                ('manufacture', models.CharField(max_length=50, null=True)),
                ('model', models.CharField(max_length=50, null=True)),
                ('plant', models.CharField(max_length=10, null=True)),
                ('power', models.CharField(max_length=50, null=True)),
                ('install_date', models.DateField(null=True)),
                ('capacity', models.TextField(max_length=1000, null=True)),
                ('note', models.TextField(max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordStorage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('note', models.TextField(max_length=1000, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('req_no', models.CharField(max_length=10)),
                ('emp_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=10)),
                ('email', models.CharField(default=None, max_length=20, null=True)),
                ('phone_no', models.CharField(max_length=10)),
                ('request_date', models.DateField(null=True)),
                ('finish_datetime', models.DateTimeField(null=True)),
                ('type', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=20)),
                ('reason', models.TextField(max_length=1000, null=True)),
                ('description', models.TextField(max_length=1000)),
                ('corrective_action', models.TextField(max_length=1000, null=True)),
                ('cause', models.TextField(max_length=1000, null=True)),
                ('spare_parts', models.TextField(max_length=1000, null=True)),
                ('is_breakdown', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmsapp.machine')),
            ],
        ),
        migrations.CreateModel(
            name='SectionGroup',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('line_token', models.CharField(max_length=100, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SplindlePart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('machine', models.CharField(max_length=100, null=True)),
                ('model', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('register_date', models.DateField(null=True)),
                ('marker', models.CharField(max_length=100, null=True)),
                ('serial_no', models.CharField(max_length=100, null=True)),
                ('nose', models.CharField(max_length=100, null=True)),
                ('max_speed', models.CharField(max_length=100, null=True)),
                ('drive_type', models.CharField(max_length=100, null=True)),
                ('lubrication', models.CharField(max_length=100, null=True)),
                ('condition', models.CharField(max_length=100, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('note', models.TextField(max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('phone_no', models.CharField(max_length=20, null=True)),
                ('note', models.TextField(max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorWorkingTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField(null=True)),
                ('stop_datetime', models.DateTimeField(null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('ven', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='TotalOperationTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('time', models.IntegerField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mcg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.machinegroup')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='RequestVendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('ven', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='RequestSubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('sub_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='sg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmsapp.sectiongroup'),
        ),
        migrations.AddField(
            model_name='request',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmsapp.task'),
        ),
        migrations.CreateModel(
            name='QualityObjectiveTarget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('type', models.CharField(max_length=4)),
                ('time', models.FloatField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mcg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.machinegroup')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('pwst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.passwordstorage')),
            ],
        ),
        migrations.CreateModel(
            name='OperatorWorkingTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField(null=True)),
                ('stop_datetime', models.DateTimeField(null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MailGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_cc', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('sg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.sectiongroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MachineDowntime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField(null=True)),
                ('stop_datetime', models.DateTimeField(null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.machine')),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='mcg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmsapp.machinegroup'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=100)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
            ],
        ),
        migrations.CreateModel(
            name='EstimateWorkingTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('time', models.IntegerField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mcg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.machinegroup')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=10)),
                ('phone_no', models.CharField(max_length=10)),
                ('scheme', models.CharField(default='Light Mode', max_length=10)),
                ('sidebar', models.CharField(default='Scrollable', max_length=10)),
                ('pv_created', models.CharField(default='Request Page', max_length=20)),
                ('auto_add', models.BooleanField(default=True)),
                ('default_owt', models.CharField(default='None', max_length=20)),
                ('enable_pwst', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Costing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=1000, null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
