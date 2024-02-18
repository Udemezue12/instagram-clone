# Generated by Django 5.0.1 on 2024-02-18 11:13

import content.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_post_content_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='content/images/', validators=[content.validators.validate_file_size]),
        ),
    ]
