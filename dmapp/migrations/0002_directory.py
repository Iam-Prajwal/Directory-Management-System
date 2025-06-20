# Generated by Django 5.0.6 on 2024-05-16 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(default='0', max_length=200)),
                ('profession', models.CharField(default='0', max_length=200)),
                ('email', models.CharField(default='0', max_length=200, unique=True)),
                ('mobilenumber', models.CharField(default='0', max_length=200)),
                ('City', models.CharField(default='0', max_length=200)),
                ('address', models.TextField(default='0', max_length=200)),
                ('status', models.CharField(default='0', max_length=1)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
