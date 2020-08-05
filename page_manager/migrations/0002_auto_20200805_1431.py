# Generated by Django 2.2.9 on 2020-08-05 12:31

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqshort',
            name='anchor',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Link do przekierowania po kliknięciu'),
        ),
        migrations.AlterField(
            model_name='faqshort',
            name='content',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faqshort',
            name='title',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Tytuł/Pytanie'),
        ),
    ]
