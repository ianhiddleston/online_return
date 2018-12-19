from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Branch(models.Model):
    branch_code = models.CharField(max_length=10, primary_key=True, )
    name = models.CharField(max_length=100, null=True)
    lo_email = models.EmailField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. UK numbers are +44 and drop leading '0'. For example +441632962499. Up to 15 digits allowed.")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    first_aider = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    next_kin_name = models.CharField(max_length=200)
    next_kin_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    next_kin_relationship = models.CharField(max_length=200)
    
    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)
    
    class Meta:
        ordering = ['user__first_name','user__last_name']

    @receiver(post_save, sender=User)
    def create_player_profile(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_player_profile(sender, instance, **kwargs):
        instance.player.save()
    
    
class Race(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    restricted = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Nationality(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    restricted = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Language(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    restricted = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Guild(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    restricted = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class GuildRank(models.Model):
    name = models.CharField(max_length=100)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    social_standing = models.PositiveIntegerField()
    restricted = models.BooleanField()
    
    def __str__(self):
        return ( self.guild.name + " " + self.name)
    
    class Meta:
        ordering = ['guild__name', 'name',]
    
class Character(models.Model):
    STATE_CHOICES = (
        ('A', 'Active'),
        ('D', 'Dead'),
        ('R', 'Retired'),
        ('N', 'NPC'),
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    started = models.DateTimeField(default=datetime.now)
    resurrected = models.BooleanField()
    excommunicated = models.BooleanField()
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language)
    guilds = models.ManyToManyField(Guild)
    guild_ranks = models.ManyToManyField(GuildRank)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return ( self.name )
    
    class Meta:
        ordering = ['name',]
