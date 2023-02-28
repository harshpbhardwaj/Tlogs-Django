# Generated by Django 3.2.16 on 2022-11-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=122)),
                ('phone', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=122)),
                ('cpassword', models.CharField(max_length=122)),
                ('city', models.CharField(max_length=90)),
                ('state', models.CharField(max_length=90)),
                ('country', models.CharField(max_length=90)),
                ('terms', models.CharField(max_length=1)),
                ('date', models.DateField()),
            ],
        ),
    ]