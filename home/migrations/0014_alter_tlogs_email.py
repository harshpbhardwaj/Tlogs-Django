# Generated by Django 3.2.16 on 2022-12-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20221216_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlogs',
            name='email',
            field=models.CharField(max_length=122),
        ),
    ]
