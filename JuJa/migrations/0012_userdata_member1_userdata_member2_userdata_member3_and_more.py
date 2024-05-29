# Generated by Django 5.0.3 on 2024-05-29 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JuJa', '0011_tablerow_column5_tablerow_column6_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='member1',
            field=models.CharField(blank=True, default='NARYS1', max_length=100),
        ),
        migrations.AddField(
            model_name='userdata',
            name='member2',
            field=models.CharField(blank=True, default='NARYS2', max_length=100),
        ),
        migrations.AddField(
            model_name='userdata',
            name='member3',
            field=models.CharField(blank=True, default='NARYS3', max_length=100),
        ),
        migrations.AddField(
            model_name='userdata',
            name='member4',
            field=models.CharField(blank=True, default='NARYS4', max_length=100),
        ),
        migrations.AddField(
            model_name='userdata',
            name='responsible_member',
            field=models.CharField(blank=True, default='ATSAKINGAS DARBUOTOJAS', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='invoice_date',
            field=models.CharField(default='2024-05-29', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='payment_date',
            field=models.CharField(default='2024-05-29', max_length=100),
        ),
    ]