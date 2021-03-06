# Generated by Django 2.1.5 on 2019-01-09 16:27

from django.db import migrations


def set_initial_order(apps, schema_editor):
    Theme = apps.get_model('control', 'Theme')
    Questionnaire = apps.get_model('control', 'Questionnaire')
    for questionnaire in Questionnaire.objects.all():
        for i, theme in enumerate(Theme.objects.filter(questionnaire=questionnaire)):
            theme.order = i
            theme.save()


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_add_order_to_theme'),
    ]

    operations = [
        migrations.RunPython(
            set_initial_order,
            reverse_code=lambda apps, schema_editor: None
        )
    ]
