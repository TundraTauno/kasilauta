# Generated by Django 2.0.10 on 2019-07-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20190711_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gallery.Board'),
        ),
    ]