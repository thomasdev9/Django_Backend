# Generated by Django 3.2.7 on 2021-09-27 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_participantslist_candidates'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('professional_experience', models.CharField(max_length=2000)),
                ('education', models.CharField(max_length=2000)),
                ('skills', models.CharField(max_length=2000)),
                ('state_profession', models.BooleanField(default=True)),
                ('state_experience', models.BooleanField(default=True)),
                ('state_education', models.BooleanField(default=True)),
                ('state_skills', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='api.userprofile')),
            ],
        ),
    ]
