# Generated by Django 2.1.5 on 2019-11-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_auto_20191123_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='dost',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
    ]
