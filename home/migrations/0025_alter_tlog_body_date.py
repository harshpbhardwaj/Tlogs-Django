# Generated by Django 3.2.16 on 2022-12-20 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_login_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlog_body',
            name='date',
            field=models.DateTimeField(),
        ),
    ]