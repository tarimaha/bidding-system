# Generated by Django 4.2.13 on 2024-05-18 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bids', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Accessories', 'Accessories'), ('Antiques', 'Antiques'), ('Clothes', 'Clothes'), ('Decoration', 'Decoration'), ('Electronics', 'Electronics'), ('Valuables', 'Valuables'), ('Valuables', 'vehicle'), ('Other', 'Other')], default='Other', max_length=11),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('payment_card_number', models.CharField(blank=True, max_length=16)),
                ('payment_expiry_date', models.DateField(blank=True, null=True)),
                ('seller_rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
