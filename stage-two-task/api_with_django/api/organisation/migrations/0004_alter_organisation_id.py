# Generated by Django 3.2.12 on 2024-07-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_auto_20240709_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='id',
            field=models.CharField(auto_created=True, default='f2db4866-a91b-4f81-84dc-09d8a123ae8a', max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
