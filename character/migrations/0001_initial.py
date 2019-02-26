# Generated by Django 2.1.3 on 2019-02-25 11:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('lo_email', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('ref', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('state', models.CharField(choices=[('A', 'Active'), ('D', 'Dead'), ('R', 'Retired'), ('N', 'NPC')], default='A', max_length=2)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('ended', models.DateTimeField(blank=True, null=True)),
                ('resurrected', models.BooleanField(default=False)),
                ('excommunicated', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('restricted', models.BooleanField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GuildRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('starting_rank', models.BooleanField()),
                ('rank', models.PositiveSmallIntegerField()),
                ('social_standing', models.PositiveIntegerField()),
                ('tithe_amount', models.IntegerField(blank=True, null=True)),
                ('tithe_percent', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('restricted', models.BooleanField()),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character.Guild')),
            ],
            options={
                'ordering': ['guild__name', 'social_standing', 'rank'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('restricted', models.BooleanField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('restricted', models.BooleanField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number should be entered in the format: '+xx9999999'. UK numbers are +44 and drop leading '0'. For example +441632962499. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('first_aider', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('emergency_contact_name', models.CharField(max_length=200)),
                ('emergency_contact_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number should be entered in the format: '+xx9999999'. UK numbers are +44 and drop leading '0'. For example +441632962499. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('emergency_contact_relationship', models.CharField(max_length=200)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='character.Branch')),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('restricted', models.BooleanField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('pennies', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(choices=[('S', 'Sold Items'), ('B', 'Bought Items'), ('P', 'Mission Pay'), ('C', 'Material Cost'), ('F', 'Fine'), ('T', 'Tithe')], max_length=2)),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Character')),
            ],
        ),
        migrations.AddField(
            model_name='guild',
            name='banned_races',
            field=models.ManyToManyField(blank=True, to='character.Race'),
        ),
        migrations.AddField(
            model_name='character',
            name='guild_ranks',
            field=models.ManyToManyField(to='character.GuildRank'),
        ),
        migrations.AddField(
            model_name='character',
            name='guilds',
            field=models.ManyToManyField(to='character.Guild'),
        ),
        migrations.AddField(
            model_name='character',
            name='languages',
            field=models.ManyToManyField(to='character.Language'),
        ),
        migrations.AddField(
            model_name='character',
            name='nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Nationality'),
        ),
        migrations.AddField(
            model_name='character',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Player'),
        ),
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Race'),
        ),
        migrations.AddField(
            model_name='cash',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Character'),
        ),
    ]
