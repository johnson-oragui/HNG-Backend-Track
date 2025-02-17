# Generated by Django 3.2.12 on 2024-07-08 23:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0002_alter_organisation_id'),
        ('user', '0011_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrganisation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateField(default=django.utils.timezone.now)),
                ('update_at', models.DateField(default=django.utils.timezone.now)),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('member', 'Member')], default='owner', max_length=60)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_organisations',
                'unique_together': {('user', 'organisation')},
            },
        ),
    ]
