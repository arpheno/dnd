# Generated by Django 2.1.5 on 2019-02-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encounter', '0003_auto_20190225_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
