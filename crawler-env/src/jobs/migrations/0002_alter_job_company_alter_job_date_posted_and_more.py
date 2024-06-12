# Generated by Django 5.0.6 on 2024-06-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='date_posted',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='summary',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='url',
            field=models.TextField(null=True),
        ),
    ]