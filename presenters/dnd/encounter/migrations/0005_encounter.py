# Generated by Django 2.1.5 on 2019-02-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encounter', '0004_character_race'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.TextField(default='[]')),
                ('map', models.TextField(default='[]')),
            ],
        ),
    ]
