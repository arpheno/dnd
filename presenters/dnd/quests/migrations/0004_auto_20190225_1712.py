# Generated by Django 2.1.5 on 2019-02-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0003_auto_20190208_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='adventure',
            field=models.ForeignKey(on_delete='cascade', related_name='quests', to='quests.Adventure'),
        ),
    ]
