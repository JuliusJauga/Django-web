# Generated by Django 5.0.3 on 2024-05-19 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JuJa', '0002_usertable_tablerow_delete_item_delete_todolist'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablerow',
            name='column4',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
