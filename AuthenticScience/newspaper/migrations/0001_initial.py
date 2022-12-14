# Generated by Django 3.0.5 on 2022-10-18 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleDetailsRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('title_requested', models.CharField(max_length=100)),
                ('id_string', models.CharField(max_length=10)),
                ('pk_requested', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_date', models.DateTimeField(verbose_name='time of login')),
                ('ip_address', models.GenericIPAddressField()),
                ('user_logged', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified_author', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(default='if you are curious read my content!', max_length=300)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('D', 'draft'), ('P', 'Published'), ('W', 'Withdrawn')], default='D', max_length=1)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('tx_id', models.CharField(blank=True, max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
