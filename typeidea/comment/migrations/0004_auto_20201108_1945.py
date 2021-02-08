# Generated by Django 3.1.3 on 2020-11-08 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20201103_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'NORMAL'), (0, 'DELETE')], db_index=True, default=1, verbose_name='status'),
        ),
    ]