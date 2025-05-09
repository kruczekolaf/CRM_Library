# Generated by Django 5.2 on 2025-05-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_borrowedbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='fee_paid',
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='borrowed_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='returned_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
