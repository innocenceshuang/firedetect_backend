# Generated by Django 3.2 on 2021-05-16 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0003_auto_20210516_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='status',
            field=models.CharField(default='offline', max_length=20),
        ),
    ]