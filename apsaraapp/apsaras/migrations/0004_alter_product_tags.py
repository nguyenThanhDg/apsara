# Generated by Django 4.0.2 on 2022-07-28 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apsaras', '0003_productview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='apsaras.Tag'),
        ),
    ]