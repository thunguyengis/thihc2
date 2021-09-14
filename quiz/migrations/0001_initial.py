# Generated by Django 3.0 on 2021-08-28 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0001_initial'),
        ('configurations', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOfStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.TextField(null=True)),
                ('choice_index', models.TextField(null=True)),
                ('order', models.IntegerField(default=0)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
