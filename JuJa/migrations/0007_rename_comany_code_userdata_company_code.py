# Generated by Django 5.0.3 on 2024-05-19 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JuJa', '0006_userdata_comany_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='comany_code',
            new_name='company_code',
        ),
    ]
