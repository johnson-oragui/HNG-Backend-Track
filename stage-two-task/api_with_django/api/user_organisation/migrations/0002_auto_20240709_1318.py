# Generated by Django 3.2.12 on 2024-07-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_organisation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorganisation',
            name='user_org_id',
            field=models.CharField(default='ef047c1a-b58c-4d21-b3d6-5bd3d902ce0d', max_length=60),
        ),
        migrations.AlterField(
            model_name='userorganisation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
