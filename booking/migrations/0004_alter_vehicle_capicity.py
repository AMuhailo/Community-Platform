# Generated by Django 5.1.7 on 2025-04-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='capicity',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
