# Generated by Django 4.2.7 on 2024-01-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_bookinstance_borrower_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Maintenance'), ('r', 'Reserved'), ('a', 'Available'), ('o', 'On loan')], default='m', help_text='Book availability', max_length=1),
        ),
    ]
