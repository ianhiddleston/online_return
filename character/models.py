from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number should be entered in the format: '+xx9999999'. UK numbers are +44 and drop leading '0'. For example +441632962499. Up to 15 digits allowed.")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    first_aider = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    registered = models.DateTimeField(default=now)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    emergency_contact_relationship = models.CharField(max_length=200)

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

class SocialPosition(models.Model):
    #This modifier allows a character to accumulate additional
    name = models.CharField(max_length=100, primary_key=True)
    social_change = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    at_branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

class Guild(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    restricted = models.BooleanField()
    banned_races = models.ManyToManyField(Race, blank=True)
    
    def starting_rank(self):
        return GuildRank.objects.filter(guild=self, starting_rank=True).first()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class GuildRank(models.Model):
    name = models.CharField(max_length=100)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    starting_rank = models.BooleanField()
    rank = models.PositiveSmallIntegerField()
    social_standing = models.PositiveIntegerField()
    tithe_amount = models.IntegerField(null=True, blank=True)
    tithe_percent = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    restricted = models.BooleanField()

    def __str__(self):
        return ( self.guild.name + " " + self.name)

    class Meta:
        ordering = ['guild__name', 'social_standing', 'rank']

    def next_rank(self, guild, current_rank=None):
        # Returns the next available guild rank.
        # May be restricted so unable to advance without permission.
        if current_rank is None:
            return starting_rank(guild)
        else:
            #Find the next highest rank in the guild, this is the next one available.
            #If maximum rank has been reached in the guild then return the current rank.
            #May return a restricted rank, the player may not advance to this without permission.
            return GuildRank.objects.filter(guild=guild, rank__gte=current_rank).order_by('rank')[:1]



class Character(models.Model):
    ACTIVE = 'A'
    DEAD = 'D'
    RETIRED = 'R'
    NPC = 'N'
    MAX_GUILDS = 5
    STATE_CHOICES = (
        (ACTIVE, 'Active'),
        (DEAD, 'Dead'),
        (RETIRED, 'Retired'),
        (NPC, 'NPC'),
    )
    ref = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=ACTIVE)
    started = models.DateTimeField(default=now)
    ended = models.DateTimeField(null=True, blank=True)
    resurrected = models.BooleanField(default=False)
    resurrected_on = models.DateTimeField(null=True, blank=True)
    excommunicated = models.BooleanField(default=False)
    excommunicated_on = models.DateTimeField(null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    nationality = models.ForeignKey(Nationality, on_delete=models.PROTECT)
    languages = models.ManyToManyField(Language)
    guilds = models.ManyToManyField(Guild)
    guild_ranks = models.ManyToManyField(GuildRank)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return ( self.name )

    def is_active(self):
        return self.state == Character.ACTIVE

    def is_dead(self):
        return self.state == Character.DEAD

    def is_retired(self):
        return self.state == Character.RETIRED

    def is_npc(self):
        return self.state == Character.NPC

    def is_excommunicated(self):
        return self.excommunicated

    def retire(self):
        if self.is_active() :
            self.state = Character.RETIRED
            self.ended = now()
        else :
            raise Exception("Character is not active so cannot retire.")

    def die(self):
        if not self.is_dead():
            self.state = Character.DEAD
            self.ended = now()
        else:
            raise Exception("Character is already dead.")
    
    def resurrect(self):
        if self.resurrected:
            raise Exception("Characters cannot be resurrected more than once. Please contact an admin.")
        if self.is_dead():
            self.state = Character.ACTIVE
            self.resurrected_on = now()
            self.resurrected = True
        else:
            raise Exception("Unexpected error, you don't appear to need resurrection.")
    
    def excommunicate(self):
        if self.excommunicated:
            raise Exception("Character is already excommunicated. Please contact an admin.")
        else:
            self.excommunicated_on = now()
            self.excommunicated = True

    def turn_npc(self):
        if not self.is_dead():
            self.state = Character.NPC
        else:
            raise Exception("Character is already dead.")
        if self.ended == None:
            self.ended = now()
    
    def get_social_modifier(self, branch=None):
        #Returns the total social modifier
        total_modifier = 0
        socialpositions = self.socialposition_set.all()
        for position in socialpositions:
            if branch is not None:
                if position.at_branch == branch:
                    total_modifier += position.social_change
            else:
                if position.at_branch is None:
                    total_modifier += position.social_change
        return total_modifier
            
    
    def get_brands(self):
        return self.brand_set.all()
    
    def get_social(self, guild=None):
        if self.excommunicated:
            #Excommunicated characters have a social standing of 1.
            return 1
        if Guild is not None:
            #Get the highest rank in the specified guild and return the social from that plus any modifier.
            #Note the order_by is descending, it'll return only the guild_rank with the highest social standing.
            guild_rank = self.guild_ranks.filter(guild=guild).order_by('-social_standing').first()
            social_standing = guild_rank.social_standing
        else:
            highest_standing = self.guild_ranks.all().aggregate(Max('social_standing'))
            social_standing = highest_standing
            if social_standing is None:
                social_standing = 2
        return social_standing

    def join_guild(self, guild):
        number_guilds = self.guilds.count()
        if number_guilds < Character.MAX_GUILDS:
            self.guilds.add(guild)
            self.guild_ranks.add(GuildRank.next_rank(guild))
        else:
            raise Exception("Character a member of too many guilds: " + str(current_guilds))

    def leave_guild(self, guild):
        self.guilds.remove(guild)

    class Meta:
        ordering = ['name',]


class Brand(models.Model):
    reason = models.CharField(max_length=100, primary_key=True)
    applied_on = models.DateTimeField(null=True, blank=True)
    applied_to = models.ForeignKey(Character, null=True, blank=True, on_delete=models.CASCADE)

class Cash(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT)
    balance = models.IntegerField(default=0)

    def _balance(self):
        aggregates = self.character.transaction_set.aggregate(sum=Sum('pennies'))
        sum = aggregates['sum']
        return 0 if sum is None else sum
    def save(self, *args, **kwargs):
        # Ensure the balance is always current when saving
        self.balance = self._balance()
        return super(Model, self).save(*args, **kwargs)

class Transaction(models.Model):
    # Track income vs expenditure.
    # Track whether for mission pay or goods or service
    # Track when it occured.

    SOLD_ITEMS = 'S'
    BOUGHT_ITEMS = 'B'
    MISSION_PAY = 'P'
    MATERIAL_COST = 'C'
    STARTING_CASH = 'I'
    FINE = 'F'
    TITHE = 'T'
    STATE_CHOICES = (
        (SOLD_ITEMS, 'Sold Items'),
        (BOUGHT_ITEMS, 'Bought Items'),
        (MISSION_PAY, 'Mission Pay'),
        (MATERIAL_COST, 'Material Cost'),
        (STARTING_CASH, 'Starting Cash'),
        (FINE, 'Fine'),
        (TITHE, 'Tithe'),
    )
    pennies = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=2, choices=STATE_CHOICES)
    reference=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return u"Ref: %s, amount: %.2f" % (
            self.transaction_type, self.pennies)

    def to_crowns(self):
        #12 pence to the crown. Output as Crowns and Pence, actually only work with pence because fuck base 12.
        crowns = self.pennies // 12
        pence = self.pennies % 12
        return "{0}/{1}".format(crowns, pence)

    def delete(self, *args, **kwargs):
        raise RuntimeError("Transactions cannot be deleted")

class Adventure(models.Model):
    SOCIAL = 'S'
    FIXED = 'F'
    MILITIA = 'M'
    SOCIAL_BONUS = 'SF'
    STATE_CHOICES = (
        (SOCIAL, 'Social'),
        (FIXED, 'Fixed'),
        (MILITIA, 'Militia Duty'),
        (SOCIAL_BONUS, 'Social plus Bonus'),
    )
    date = models.DateField(default=date.today)
    social = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    social_overridden = models.BooleanField(default=False)
    bonus_amount = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(200)])
    total_amount = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(200)])
    total_overridden = models.BooleanField(default=False)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    notes = models.TextField(null=True, blank=True)
    reference = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Ensure the balance is always current when saving
        self.balance = self._balance()
        return super(Model, self).save(*args, **kwargs)
