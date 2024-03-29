# Generated by Django 4.2.7 on 2024-01-08 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available'), ('r', 'Reserved'), ('o', 'On loan'), ('m', 'Maintenance')], default='m', help_text='Book availability', max_length=1),
        ),
    ]
