# Generated by Django 2.1.2 on 2019-04-15 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_team', '0003_auto_20190415_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teaminfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='teaminfo',
            name='player_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='manage_team.PlayerInfo'),
        ),
        migrations.AlterField(
            model_name='teaminfo',
            name='team_name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='teaminfo',
            name='team_points',
            field=models.IntegerField(default=0),
        ),
    ]