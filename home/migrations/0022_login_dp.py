# Generated by Django 3.2.16 on 2022-12-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_tlog_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='dp',
            field=models.TextField(blank=True, null=True),
        ),
    ]
