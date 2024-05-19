# Generated by Django 5.0.6 on 2024-05-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=200)),
                ('user_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='passwords',
            name='email',
        ),
        migrations.DeleteModel(
            name='Emails',
        ),
        migrations.DeleteModel(
            name='Passwords',
        ),
    ]