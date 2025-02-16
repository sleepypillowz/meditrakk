# Generated by Django 5.1.5 on 2025-02-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queueing', '0002_temporarystoragequeue_queue_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='preliminaryassessment',
            name='alcohol_use',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='allergies',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='current_medications',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='current_symptoms',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='medical_history',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='pain_location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='pain_scale',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='preliminaryassessment',
            name='smoking_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
