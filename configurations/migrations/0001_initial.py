# Generated by Django 3.0 on 2021-08-28 05:55

import configurations.models
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
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200, null=True)),
                ('year_begins', models.IntegerField(default=2021, validators=[configurations.models.min_value_current_year, configurations.models.max_value_current_year])),
                ('year_end', models.IntegerField(default=2021, validators=[configurations.models.min_value_current_year, configurations.models.max_value_current_year])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Configurations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('established', models.CharField(max_length=200, null=True)),
                ('about', models.TextField(default='-', null=True)),
                ('medium', models.CharField(max_length=200, null=True)),
                ('code', models.IntegerField(null=True, unique=True)),
                ('theme', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200, null=True)),
                ('course_time', models.CharField(max_length=200, null=True)),
                ('grade_system_name', models.CharField(max_length=200, null=True)),
                ('quiz_count', models.IntegerField(default=0)),
                ('assignment_count', models.IntegerField(default=0)),
                ('ct_count', models.IntegerField(default=0)),
                ('quiz_percent', models.IntegerField(default=0)),
                ('attendance_percent', models.IntegerField(default=0)),
                ('assignment_percent', models.IntegerField(default=0)),
                ('ct_percent', models.IntegerField(default=0)),
                ('final_exam_percent', models.IntegerField(default=0)),
                ('practical_percent', models.IntegerField(default=0)),
                ('att_fullmark', models.IntegerField(default=0)),
                ('quiz_fullmark', models.IntegerField(default=0)),
                ('ct_fullmark', models.IntegerField(default=0)),
                ('final_fullmark', models.IntegerField(default=0)),
                ('practical_fullmark', models.IntegerField(default=0)),
                ('a_fullmark', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOfSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200, null=True)),
                ('course_time', models.CharField(max_length=200, null=True)),
                ('grade_system_name', models.CharField(max_length=200, null=True)),
                ('quiz_count', models.IntegerField(default=0)),
                ('assignment_count', models.IntegerField(default=0)),
                ('ct_count', models.IntegerField(default=0)),
                ('quiz_percent', models.IntegerField(default=0)),
                ('attendance_percent', models.IntegerField(default=0)),
                ('assignment_percent', models.IntegerField(default=0)),
                ('ct_percent', models.IntegerField(default=0)),
                ('final_exam_percent', models.IntegerField(default=0)),
                ('practical_percent', models.IntegerField(default=0)),
                ('att_fullmark', models.IntegerField(default=0)),
                ('quiz_fullmark', models.IntegerField(default=0)),
                ('ct_fullmark', models.IntegerField(default=0)),
                ('final_fullmark', models.IntegerField(default=0)),
                ('practical_fullmark', models.IntegerField(default=0)),
                ('a_fullmark', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200, null=True, verbose_name='C?? quan')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Majors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('majors_name', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('picpath', models.ImageField(null=True, upload_to='uploads')),
                ('order', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('religion', models.CharField(max_length=200, null=True)),
                ('picpath', models.ImageField(null=True, upload_to='uploads')),
                ('gender', models.CharField(max_length=100, null=True)),
                ('year_begins', models.IntegerField(default=2021)),
                ('order', models.IntegerField(default=0)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GradeOfVN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_mark_exam', models.FloatField(default=0, null=True)),
                ('total_mark_course', models.FloatField(default=0, null=True)),
                ('total_marks', models.FloatField(default=0, null=True)),
                ('coefficient_1_1', models.FloatField(default=0, null=True)),
                ('coefficient_1_2', models.FloatField(default=0, null=True)),
                ('coefficient_v2_1_1', models.FloatField(default=0, null=True)),
                ('coefficient_v2_1_2', models.FloatField(default=0, null=True)),
                ('coefficient_2_1', models.FloatField(default=0, null=True)),
                ('coefficient_2_2', models.FloatField(default=0, null=True)),
                ('coefficient_v2_2_1', models.FloatField(default=0, null=True)),
                ('coefficient_v2_2_2', models.FloatField(default=0, null=True)),
                ('practical_1_1', models.FloatField(default=0, null=True, verbose_name='Th???c h??nh')),
                ('practical_v2_1_1', models.FloatField(default=0, null=True, verbose_name='Th???c h??nh')),
                ('end_mark_1_1', models.FloatField(default=0, null=True)),
                ('end_mark_v2_1_1', models.FloatField(default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('courseOfSection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.CourseOfSection')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Teacher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField(default=0, null=True)),
                ('attendance', models.FloatField(default=0, null=True)),
                ('quiz1', models.FloatField(default=0, null=True)),
                ('quiz2', models.FloatField(default=0, null=True)),
                ('quiz3', models.FloatField(default=0, null=True)),
                ('quiz4', models.FloatField(default=0, null=True)),
                ('quiz5', models.FloatField(default=0, null=True)),
                ('ct1', models.FloatField(default=0, null=True)),
                ('ct2', models.FloatField(default=0, null=True)),
                ('ct3', models.FloatField(default=0, null=True)),
                ('ct4', models.FloatField(default=0, null=True)),
                ('ct5', models.FloatField(default=0, null=True)),
                ('assignment1', models.FloatField(default=0, null=True)),
                ('assignment2', models.FloatField(default=0, null=True)),
                ('assignment3', models.FloatField(default=0, null=True)),
                ('written', models.FloatField(default=0, null=True)),
                ('mcq', models.FloatField(default=0, null=True)),
                ('practical', models.FloatField(default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Teacher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picpath', models.ImageField(null=True, upload_to='uploads/% Y/% m/% d/')),
                ('gender', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursOfDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200, null=True, verbose_name='M??n Gi???ng D???y')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('order', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Department')),
            ],
        ),
        migrations.AddField(
            model_name='courseofsection',
            name='coursOfDepartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.CoursOfDepartment'),
        ),
        migrations.AddField(
            model_name='courseofsection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Section'),
        ),
        migrations.AddField(
            model_name='courseofsection',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Teacher'),
        ),
        migrations.AddField(
            model_name='courseofsection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Section'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Teacher'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='class',
            name='majors',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Majors'),
        ),
    ]
