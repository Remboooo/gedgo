# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gedgo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentary',
            name='thumb',
            field=models.ForeignKey(related_name='documentaries_thumb', blank=True, to='gedgo.Document', null=True, on_delete=models.DO_NOTHING),
            preserve_default=True,
        ),
    ]
