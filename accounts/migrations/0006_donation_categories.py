# Generated by Django 4.0.4 on 2022-05-24 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_donation_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(to='accounts.category'),
        ),
    ]
