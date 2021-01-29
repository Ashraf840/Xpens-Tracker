# Generated by Django 3.1.5 on 2021-01-28 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensesapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name_plural': 'Expense'},
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
