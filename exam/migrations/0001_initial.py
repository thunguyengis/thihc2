# Generated by Django 3.0 on 2021-08-28 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configurations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=200, null=True)),
                ('exam_name', models.CharField(max_length=200, null=True)),
                ('exam_type2', models.CharField(max_length=50, null=True)),
                ('exam_code', models.CharField(max_length=50, null=True)),
                ('active', models.BooleanField(default=False)),
                ('notice_published', models.BooleanField(default=False)),
                ('result_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('time_exam', models.IntegerField(default=90)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.IntegerField(default=0)),
                ('courseOfSection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.CourseOfSection')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=200, null=True, verbose_name='Cơ quan')),
                ('room_number_test', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GradeOfExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField(default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('doing_exam', models.BooleanField(default=False)),
                ('starting_time', models.DateTimeField(editable=False, null=True)),
                ('time_remaining', models.CharField(max_length=50, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Exam')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
