# Generated by Django 4.1.3 on 2023-02-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_alter_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=True),
        ),
    ]