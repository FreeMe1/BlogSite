# Generated by Django 2.0 on 2018-02-12 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_articles_updatetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='UpdateTime',
            field=models.CharField(default='', max_length=50),
        ),
    ]