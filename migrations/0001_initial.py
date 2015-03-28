# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('docfile', models.FileField(upload_to=b'uploaded')),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('thumb', models.FileField(null=True, upload_to=b'uploaded/thumbs', blank=True)),
                ('kind', models.CharField(max_length=5, choices=[(b'DOCUM', b'Document'), (b'VIDEO', b'Video'), (b'PHOTO', b'Image')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Documentary',
            fields=[
                ('title', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('tagline', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Documentaries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True)),
                ('year_range_end', models.IntegerField(null=True)),
                ('date_format', models.CharField(max_length=10, null=True)),
                ('date_approxQ', models.BooleanField(verbose_name=b'Date is approximate')),
                ('place', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('pointer', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('kind', models.CharField(max_length=10, null=True, verbose_name=b'Event', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gedcom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=40, null=True, blank=True)),
                ('title', models.CharField(max_length=40, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('last_updated', models.DateTimeField()),
                ('key_families', models.ManyToManyField(related_name='gedcom_key_families', null=True, to='gedgo.Family', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('pointer', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('text', models.TextField()),
                ('gedcom', models.ForeignKey(to='gedgo.Gedcom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('pointer', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('prefix', models.CharField(max_length=255)),
                ('suffix', models.CharField(max_length=255)),
                ('education', models.TextField(null=True)),
                ('religion', models.CharField(max_length=255, null=True, blank=True)),
                ('birth', models.ForeignKey(related_name='person_birth', blank=True, to='gedgo.Event', null=True)),
                ('child_family', models.ForeignKey(related_name='person_child_family', blank=True, to='gedgo.Family', null=True)),
                ('death', models.ForeignKey(related_name='person_death', blank=True, to='gedgo.Event', null=True)),
                ('gedcom', models.ForeignKey(to='gedgo.Gedcom')),
                ('notes', models.ManyToManyField(to='gedgo.Note', null=True)),
                ('profile', models.ManyToManyField(to='gedgo.Document', null=True, blank=True)),
                ('spousal_families', models.ManyToManyField(related_name='person_spousal_families', to='gedgo.Family')),
            ],
            options={
                'verbose_name_plural': 'People',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gedcom',
            name='key_people',
            field=models.ManyToManyField(related_name='gedcom_key_people', null=True, to='gedgo.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='children',
            field=models.ManyToManyField(related_name='family_children', to='gedgo.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='gedcom',
            field=models.ForeignKey(to='gedgo.Gedcom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='husbands',
            field=models.ManyToManyField(related_name='family_husbands', to='gedgo.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='joined',
            field=models.ForeignKey(related_name='family_joined', blank=True, to='gedgo.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='notes',
            field=models.ManyToManyField(to='gedgo.Note', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='separated',
            field=models.ForeignKey(related_name='family_separated', blank=True, to='gedgo.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='wives',
            field=models.ManyToManyField(related_name='family_wives', to='gedgo.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='gedcom',
            field=models.ForeignKey(to='gedgo.Gedcom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentary',
            name='gedcom',
            field=models.ForeignKey(to='gedgo.Gedcom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentary',
            name='tagged_families',
            field=models.ManyToManyField(related_name='documentaries_tagged_families', null=True, to='gedgo.Family', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentary',
            name='tagged_people',
            field=models.ManyToManyField(related_name='documentaries_tagged_people', null=True, to='gedgo.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentary',
            name='thumb',
            field=models.ForeignKey(related_name='documentaries_thumb', blank=True, to='gedgo.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='gedcom',
            field=models.ForeignKey(blank=True, to='gedgo.Gedcom', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='tagged_families',
            field=models.ManyToManyField(related_name='media_tagged_families', null=True, to='gedgo.Family', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='tagged_people',
            field=models.ManyToManyField(related_name='media_tagged_people', null=True, to='gedgo.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tagged_people',
            field=models.ManyToManyField(related_name='blogpost_tagged_people', null=True, to='gedgo.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tagged_photos',
            field=models.ManyToManyField(related_name='blogpost_tagged_photos', null=True, to='gedgo.Document', blank=True),
            preserve_default=True,
        ),
    ]
