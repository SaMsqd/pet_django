# Generated by Django 5.1.1 on 2024-10-06 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(auto_created=True, help_text='А нехуй сюда лезть', primary_key=True, serialize=False),
        ),
    ]
