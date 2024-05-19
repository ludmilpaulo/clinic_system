# Generated by Django 5.0.3 on 2024-05-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='doctoravailability',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='doctoravailability',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctoravailability',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='doctoravailability',
            unique_together={('doctor', 'days_of_week', 'start_time', 'end_time', 'year', 'month', 'recurring_monthly')},
        ),
    ]
