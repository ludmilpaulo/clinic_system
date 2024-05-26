# Generated by Django 5.0.3 on 2024-05-25 10:36

import django.db.models.deletion
import django_ckeditor_5.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, max_length=3000, upload_to='drug_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drugs', to='pharmacy.consultationcategory')),
                ('images', models.ManyToManyField(to='pharmacy.image')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.cart')),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drug')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='drugs',
            field=models.ManyToManyField(through='pharmacy.CartItem', to='pharmacy.drug'),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('prescription_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patientprofile')),
                ('prescribed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriber', to='accounts.doctorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionDrug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drug')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.prescription')),
            ],
        ),
        migrations.AddField(
            model_name='prescription',
            name='drugs',
            field=models.ManyToManyField(through='pharmacy.PrescriptionDrug', to='pharmacy.drug'),
        ),
    ]
