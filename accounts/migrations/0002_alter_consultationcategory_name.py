# Generated by Django 5.0.3 on 2024-05-15 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultationcategory',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
