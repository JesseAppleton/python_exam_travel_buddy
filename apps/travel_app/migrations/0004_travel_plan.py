# Generated by Django 2.2.3 on 2019-07-22 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0003_auto_20190722_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='plan',
            field=models.CharField(default='A cool trip!', max_length=255),
            preserve_default=False,
        ),
    ]