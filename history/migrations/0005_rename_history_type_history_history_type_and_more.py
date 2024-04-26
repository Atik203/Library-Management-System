# Generated by Django 5.0.4 on 2024-04-26 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_alter_history_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='History_type',
            new_name='history_type',
        ),
        migrations.AlterField(
            model_name='history',
            name='balance_after_borrow',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='balance_after_return',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
