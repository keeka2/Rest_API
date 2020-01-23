# Generated by Django 2.2.4 on 2019-09-01 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageId', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=128)),
                ('price', models.CharField(max_length=8)),
                ('gender', models.CharField(max_length=8)),
                ('category', models.CharField(max_length=16)),
                ('ingredients', models.CharField(max_length=128)),
                ('monthlySales', models.IntegerField()),
                ('oilyRating',models.IntegerField(default=0)),
                ('dryRating', models.IntegerField(default=0)),
                ('sensitiveRating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(max_length=32)),
                ('oily', models.CharField(max_length=1, default='p')),
                ('dry', models.CharField(max_length=1, default='p')),
                ('sensitive', models.CharField(max_length=1, default='p')),
            ],
        ),
    ]
