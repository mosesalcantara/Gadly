# Generated by Django 4.1.3 on 2023-12-13 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_delete_synonyms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Synset',
            fields=[
                ('synset_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('synset_name', models.CharField(max_length=255)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.word')),
            ],
        ),
    ]
