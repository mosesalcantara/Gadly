# Generated by Django 4.1.3 on 2023-05-24 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_user_reset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='reset',
            new_name='token',
        ),
    ]
