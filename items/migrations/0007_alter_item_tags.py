# Generated by Django 5.0.7 on 2024-08-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_remove_item_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(null=True, to='items.tag'),
        ),
    ]
