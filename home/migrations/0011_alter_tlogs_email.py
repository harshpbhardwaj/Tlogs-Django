# Generated by Django 3.2.16 on 2022-12-16 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_tlogs_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlogs',
            name='email',
            field=models.CharField(max_length=122),
        ),
    ]
    # operations = [
    #     migrations.RenameField(
    #         model_name='Tlogs',
    #         old_name='email',
    #         new_name='email_id',
    #     ),
    # ]
