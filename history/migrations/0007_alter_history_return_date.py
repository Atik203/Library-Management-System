# Generated by Django 5.0.4 on 2024-04-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0006_alter_history_borrow_date_alter_history_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='return_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
