# Generated by Django 3.1.4 on 2023-01-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.TextField(max_length=100)),
                ('apellido_paterno', models.TextField(max_length=50)),
                ('apellido_materno', models.TextField(max_length=50)),
                ('dni', models.TextField(max_length=8)),
            ],
        ),
    ]
