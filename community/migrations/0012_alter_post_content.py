# Generated by Django 3.2.21 on 2023-11-07 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0011_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
