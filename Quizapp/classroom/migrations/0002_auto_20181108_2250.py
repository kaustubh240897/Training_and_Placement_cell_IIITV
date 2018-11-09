# Generated by Django 2.1.2 on 2018-11-08 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'verbose_name_plural': 'Job'},
        ),
        migrations.AlterModelOptions(
            name='organizationaldetails',
            options={'verbose_name_plural': 'OrganizationalDetail'},
        ),
        migrations.AlterModelOptions(
            name='personaldetails',
            options={'verbose_name_plural': 'PersonalDetail'},
        ),
        migrations.RenameField(
            model_name='job',
            old_name='org',
            new_name='organization',
        ),
        migrations.RemoveField(
            model_name='organizationaldetails',
            name='personal_detail',
        ),
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='organization',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_details', to='classroom.OrganizationalDetails'),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]