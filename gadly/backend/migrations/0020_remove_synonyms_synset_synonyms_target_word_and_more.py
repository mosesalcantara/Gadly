# Generated by Django 4.1.3 on 2024-02-19 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_synonyms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='synonyms',
            name='synset',
        ),
        migrations.AddField(
            model_name='synonyms',
            name='target_word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.word'),
        ),
        migrations.DeleteModel(
            name='Synset',
        ),
    ]