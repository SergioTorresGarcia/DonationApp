# Generated by Django 4.0.4 on 2022-05-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_donation_pick_up_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(blank=True, default='Brak uwag'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(),
        ),
    ]