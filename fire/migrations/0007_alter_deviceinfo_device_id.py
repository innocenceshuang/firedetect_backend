# Generated by Django 3.2 on 2021-05-16 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0006_alter_deviceinfo_device_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='device_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
