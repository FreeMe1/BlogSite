# Generated by Django 2.0 on 2018-01-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_essay_changedtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='Tag',
            field=models.CharField(default='default', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='Nick',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
