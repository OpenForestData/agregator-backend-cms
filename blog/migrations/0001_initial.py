# Generated by Django 2.2.9 on 2020-07-29 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15)),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tag')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tagi',
            },
        ),
        migrations.CreateModel(
            name='BlogFront',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tytuł')),
                ('title_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_for_blog_top', to=settings.FILER_IMAGE_MODEL, verbose_name='Obrazek górny')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_index_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
            ],
            options={
                'verbose_name': 'Blog Top',
                'verbose_name_plural': 'Blog Top',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15)),
                ('title_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tytuł')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('desc', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Opis do listy')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Content wpisu - <name> zostanie zamienione na imię')),
                ('movie_youtube_link', models.CharField(blank=True, max_length=120, null=True, verbose_name='Link do filmu na YT')),
                ('slug', models.SlugField()),
                ('image_in_list', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_in_list', to=settings.FILER_IMAGE_MODEL, verbose_name='Obrazek na liście bloga')),
                ('keywords', models.ManyToManyField(related_name='blog_articles', to='blog.BlogKeyword')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
            ],
            options={
                'verbose_name': 'Artykuł',
                'verbose_name_plural': 'Artykuły',
            },
        ),
    ]
