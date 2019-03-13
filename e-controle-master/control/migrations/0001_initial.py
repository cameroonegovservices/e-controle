# Generated by Django 2.1.3 on 2018-11-19 15:40

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0010_auto_20180414_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': 'Controle',
                'verbose_name_plural': 'Controles',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('description', models.TextField(max_length=255, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('theme', 'order'),
            },
        ),
        migrations.CreateModel(
            name='QuestionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('file', filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, to='filer.File', verbose_name='fichier')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='control.Question', verbose_name='question')),
            ],
            options={
                'verbose_name': 'Fichier Attaché',
                'verbose_name_plural': 'Fichiers Attachés',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=255, verbose_name='titre')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='échéance')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('control', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='control.Control', verbose_name='controle')),
            ],
            options={
                'verbose_name': 'Questionnaire',
                'verbose_name_plural': 'Questionnaires',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='titre')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='control.Theme')),
                ('questionnaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='control.Questionnaire', verbose_name='questionnaire')),
            ],
            options={
                'verbose_name': 'Thème',
                'verbose_name_plural': 'Thèmes',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='control.Theme', verbose_name='thème'),
        ),
    ]
