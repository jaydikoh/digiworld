# Generated by Django 5.1.6 on 2025-02-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_digimon_img_alter_digimon_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='digimon',
            name='toys',
            field=models.ManyToManyField(to='main_app.toy'),
        ),
    ]
