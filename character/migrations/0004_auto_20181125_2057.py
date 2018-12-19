# Generated by Django 2.1.3 on 2018-11-25 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0003_auto_20181125_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='guild_ranks',
            field=models.ManyToManyField(to='character.GuildRank'),
        ),
        migrations.AddField(
            model_name='guildrank',
            name='social_standing',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]
