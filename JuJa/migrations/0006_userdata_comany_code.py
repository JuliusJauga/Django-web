# Generated by Django 5.0.3 on 2024-05-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JuJa', '0005_remove_userdata_company_code_userdata_client_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='comany_code',
            field=models.CharField(blank=True, default='ĮMONĖS KODAS', max_length=100),
        ),
    ]
