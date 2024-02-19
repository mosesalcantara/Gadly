# Generated by Django 4.1.3 on 2023-12-13 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_synset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Synonyms',
            fields=[
                ('syno_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('syno_word', models.CharField(max_length=255)),
                ('synset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.synset')),
            ],
        ),
    ]