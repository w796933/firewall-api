# Generated by Django 3.2 on 2021-04-06 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminaddress',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='blockedaddress',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='blockevent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
