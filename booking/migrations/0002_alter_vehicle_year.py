# Generated by Django 5.1.7 on 2025-03-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.PositiveSmallIntegerField(default=2025),
        ),
    ]
