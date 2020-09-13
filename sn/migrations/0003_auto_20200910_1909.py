# Generated by Django 3.1.1 on 2020-09-10 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sn', '0002_auto_20200906_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_amount', models.CharField(default='-', max_length=64)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_list', models.CharField(choices=[], default='Select parameter ...', max_length=255)),
                ('last_login', models.CharField(max_length=64)),
                ('last_request', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sn.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='dislike',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_dislike'),
        ),
    ]
