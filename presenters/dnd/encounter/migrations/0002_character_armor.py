# Generated by Django 2.1.5 on 2019-02-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
        ('encounter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='armor',
            field=models.ForeignKey(null=True, on_delete='NULL', to='equipment.Armor'),
        ),
    ]
