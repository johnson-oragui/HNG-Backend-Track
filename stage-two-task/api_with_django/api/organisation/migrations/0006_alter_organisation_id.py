# Generated by Django 3.2.12 on 2024-07-09 13:35

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20240709_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='id',
            field=models.CharField(auto_created=True, default=api.utils.gen_uuid_str, max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
