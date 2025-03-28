# Generated by Django 5.1.4 on 2025-03-23 11:11

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(5)])),
                ('short_desc', models.CharField(max_length=255)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pet_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8)])),
                ('phone', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(5)])),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(max_length=100)),
                ('pet_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animalSearch.pet_type')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='animalSearch.user')),
            ],
        ),
        migrations.CreateModel(
            name='Pet_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100, null=True)),
                ('size', models.CharField(max_length=50)),
                ('special_marks', models.CharField(max_length=255)),
                ('picture', models.URLField(null=True)),
                ('public_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('change_date', models.DateTimeField(auto_now=True, null=True)),
                ('report_type', models.CharField(choices=[('lost', 'Потеряно'), ('found', 'Найдено')], max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('pet_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animalSearch.pet_type')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animalSearch.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animalSearch.user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_messages', to='animalSearch.user')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_messages', to='animalSearch.user')),
            ],
        ),
    ]
