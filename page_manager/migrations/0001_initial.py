# Generated by Django 2.2.9 on 2020-09-28 06:38

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
            name='AboutUsPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tytuł')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(verbose_name='Content wpisu')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='about_page_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
            ],
            options={
                'verbose_name': 'Blog Top',
                'verbose_name_plural': 'Blog Top',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccordionPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tytuł')),
                ('title_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Content wpisu')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accordion_page_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
            ],
            options={
                'verbose_name': 'Blog Top',
                'verbose_name_plural': 'Blog Top',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FaqShort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15)),
                ('title', models.CharField(blank=True, max_length=120, null=True, verbose_name='Tytuł/Pytanie')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True)),
                ('anchor', models.CharField(blank=True, max_length=500, null=True, verbose_name='Link do przekierowania po kliknięciu')),
                ('order', models.IntegerField(default='1', max_length=10, verbose_name='Kolejność')),
            ],
            options={
                'verbose_name': 'Paytanie i odpowiedź',
                'verbose_name_plural': 'Pytania i odpowiedzi',
            },
        ),
        migrations.CreateModel(
            name='PagePattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_us', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='about_us', to='page_manager.AboutUsPage', verbose_name='Szablon o Nas')),
                ('accordion', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accordion', to='page_manager.AccordionPage', verbose_name='Szablon z Akordionami')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_patterns', to='cms.Title', unique=True, verbose_name='Strona')),
            ],
            options={
                'verbose_name': 'Szablon strony',
                'verbose_name_plural': 'Szablony stron',
            },
        ),
        migrations.CreateModel(
            name='MetaTagsExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('extended_object', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
                ('public_extension', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draft_extension', to='page_manager.MetaTagsExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15)),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Tytuł')),
                ('title_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Tytuł (nadpisuje podstawowy tytuł)')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Opis (nadpisuje podstawowy opis)')),
                ('keywords_seo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('author', models.CharField(blank=True, max_length=500, null=True, verbose_name='Autor')),
                ('og_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Og:Type - według dokumentacji: https://ogp.me/')),
                ('title_slider', models.CharField(max_length=120, verbose_name='Tytuł duży')),
                ('title_slider_small', models.CharField(max_length=120, verbose_name='Tytuł mały')),
                ('contact_content', models.TextField(verbose_name='Tekst do kontaktu')),
                ('youtube_title', models.CharField(max_length=120, verbose_name='Nazwa sekcji YouTube')),
                ('youtube_link', models.CharField(max_length=500, verbose_name='Link do filmu na YouTube')),
                ('youtube_mobie_text', models.CharField(max_length=120, verbose_name='Podpis pod filmem z YouTube')),
                ('mobile_app_title', models.CharField(max_length=120, verbose_name='Tytuł sekcji aplikacja mobilna')),
                ('mobile_app_content', models.TextField(max_length=900, verbose_name='Zawartość sekcji aplikacja mobilna')),
                ('mobile_app_cta_link', models.CharField(max_length=120, verbose_name='Link na przycisku')),
                ('mobile_app_cta_text', models.CharField(max_length=120, verbose_name='Tekst na przycisku')),
                ('mobile_app_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mobile_app_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura prezentująca aplikacje')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_page_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura w social Media')),
            ],
            options={
                'verbose_name': 'Strona główna',
                'verbose_name_plural': 'Strona główna',
            },
        ),
        migrations.CreateModel(
            name='IconSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('href', models.CharField(default='#', max_length=300, verbose_name='Link do przekierowania')),
                ('title', models.CharField(max_length=120, verbose_name='Nazwa Gatunku')),
                ('order', models.IntegerField(default=1, max_length=10, verbose_name='Kolejność')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='species_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Miniatura prezentująca gatunek')),
                ('main_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='icon_species', to='page_manager.MainPage')),
            ],
        ),
        migrations.CreateModel(
            name='Accordion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Tytuł')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(verbose_name='Content wpisu')),
                ('order', models.IntegerField(default=1, max_length=10, verbose_name='Kolejność')),
                ('accordion_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accordion_page', to='page_manager.AccordionPage')),
            ],
        ),
    ]
