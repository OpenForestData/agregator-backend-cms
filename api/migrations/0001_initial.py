# Generated by Django 2.2.9 on 2020-07-24 07:37

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddMenuLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('pl', 'pl'), ('en', 'en')], default='pl', max_length=15)),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
                ('url', models.CharField(max_length=220, verbose_name='Link')),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
            ],
            options={
                'verbose_name': 'Dodanie resource (opcje)',
                'verbose_name_plural': 'Dodanie resourców (opcje)',
            },
        ),
        migrations.CreateModel(
            name='AdvancedSearchFilterGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Nazwa pola w Dataverse')),
                ('friendly_name', models.CharField(max_length=120, verbose_name='Nazwa przyjazna')),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
            ],
            options={
                'verbose_name': 'Grupa pól filtracyjnych - wyszkiwanie zaawansowane',
                'verbose_name_plural': 'Grupy pól filtracyjnych - wyszukiwanie zaawansowane',
            },
        ),
        migrations.CreateModel(
            name='AgregatorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataverse_id', models.CharField(max_length=120, unique=True, verbose_name='Dataverse Id')),
                ('friendly_name', models.CharField(max_length=120, verbose_name='Nazwa przyjazna')),
                ('description', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True)),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
                ('dv_name', models.CharField(max_length=120, unique=True, verbose_name='DvName')),
                ('publication_date', models.CharField(max_length=10, verbose_name='Data publikacji')),
                ('dv_affiliation', models.CharField(max_length=120, verbose_name='Dataverse Affiliation')),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
                ('public', models.BooleanField(default=True, verbose_name='Publiczny')),
            ],
            options={
                'verbose_name': 'Kategoria Agregatora',
                'verbose_name_plural': 'Kategorie agregatora',
            },
        ),
        migrations.CreateModel(
            name='FilterGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Nazwa pola w Dataverse')),
                ('friendly_name', models.CharField(max_length=120, verbose_name='Nazwa przyjazna')),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
            ],
            options={
                'verbose_name': 'Grupa pól filtracyjnych',
                'verbose_name_plural': 'Grupy pól filtracyjnych',
            },
        ),
        migrations.CreateModel(
            name='FilterField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=120, unique=True, verbose_name='Nazwa pola w Dataverse')),
                ('friendly_name', models.CharField(max_length=120, verbose_name='Nazwa przyjazna')),
                ('title', models.CharField(max_length=120, verbose_name='Tytuł')),
                ('type', models.CharField(max_length=120, verbose_name='Rodzaj pola')),
                ('watermark', models.CharField(default='#', max_length=120, verbose_name='Watermark')),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
                ('public', models.BooleanField(default=True, verbose_name='Publiczny')),
                ('filter_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api.FilterGroup')),
            ],
        ),
        migrations.CreateModel(
            name='AdvancedSearchFilterField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=120, unique=True, verbose_name='Nazwa pola w Dataverse')),
                ('friendly_name', models.CharField(max_length=120, verbose_name='Nazwa przyjazna')),
                ('title', models.CharField(max_length=120, verbose_name='Tytuł')),
                ('type', models.CharField(max_length=120, verbose_name='Rodzaj pola')),
                ('watermark', models.CharField(default='#', max_length=120, verbose_name='Watermark')),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=1, verbose_name='Kolejność')),
                ('public', models.BooleanField(default=True, verbose_name='Publiczny')),
                ('filter_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api.AdvancedSearchFilterGroup')),
            ],
        ),
    ]
