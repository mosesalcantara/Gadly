# Generated by Django 4.1.3 on 2023-06-24 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_user_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='paraphrase',
            name='txt',
            field=models.TextField(default=None),
        ),
    ]