# Generated by Django 3.2.12 on 2024-07-08 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(auto_created=True, default='56f54fcf-7c5e-422a-909b-6e5ceba567a2', max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
