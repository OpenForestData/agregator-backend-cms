# Generated by Django 2.2.9 on 2020-08-05 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_manager', '0002_auto_20200805_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faqshort',
            name='main_page',
        ),
        migrations.AddField(
            model_name='faqshort',
            name='language',
            field=models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15),
        ),
    ]
