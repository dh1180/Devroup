# Generated by Django 3.2.21 on 2023-10-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_auto_20231009_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]