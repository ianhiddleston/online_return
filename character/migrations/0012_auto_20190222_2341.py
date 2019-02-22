# Generated by Django 2.1.3 on 2019-02-22 23:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0011_auto_20190222_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='reference',
        ),
        migrations.AddField(
            model_name='character',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
