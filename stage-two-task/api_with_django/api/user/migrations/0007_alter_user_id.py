# Generated by Django 3.2.12 on 2024-07-08 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(auto_created=True, default='9f732b31-9a52-4979-a200-d38382b3575e', max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
