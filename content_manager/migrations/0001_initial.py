# Generated by Django 2.2.9 on 2020-07-03 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='content_manager_sliderplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Tytuł slidera duży')),
                ('small_title', models.CharField(max_length=120, verbose_name='Tytuł slidera mały')),
                ('link', models.CharField(max_length=120, verbose_name='Link slidera')),
                ('menu_title', models.CharField(max_length=120, verbose_name='Tytuł w menu slidera')),
                ('menu_title_small', models.CharField(max_length=120, verbose_name='Tytuł szary w menu slidera')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Content po kliknięciu plusa')),
                ('content_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Zdjęcie po kliknięciu w cotntent')),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to=settings.FILER_IMAGE_MODEL, verbose_name='Zdjęcie')),
                ('slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='content_manager.SliderPlugin')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtendedPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_extra_field', models.CharField(max_length=120)),
                ('extended_object', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='cms.Title')),
                ('public_extension', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draft_extension', to='content_manager.ExtendedPage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
