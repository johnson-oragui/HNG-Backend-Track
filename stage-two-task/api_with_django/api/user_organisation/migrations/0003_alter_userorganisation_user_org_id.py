# Generated by Django 3.2.12 on 2024-07-09 13:35

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_organisation', '0002_auto_20240709_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorganisation',
            name='user_org_id',
            field=models.CharField(default=api.utils.gen_uuid_str, max_length=60),
        ),
    ]
