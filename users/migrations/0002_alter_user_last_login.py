# Generated by Django 5.1.4 on 2024-12-22 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(),
        ),
    ]