# Generated by Django 4.2.13 on 2024-05-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=40)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('hobbies', models.CharField(max_length=300)),
                ('message', models.CharField(max_length=300)),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
    ]