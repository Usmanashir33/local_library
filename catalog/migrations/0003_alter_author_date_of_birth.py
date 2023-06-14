# Generated by Django 4.2 on 2023-05-03 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_language_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, help_text='Write your date of birth e.g 14/03/2001', null=True, verbose_name='D.O.B'),
        ),
    ]