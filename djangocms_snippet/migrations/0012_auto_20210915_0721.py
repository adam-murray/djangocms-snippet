# Generated by Django 2.2.24 on 2021-09-15 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0011_cms4_plugin_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippetptr',
            name='snippet',
        ),
        migrations.AlterField(
            model_name='snippet',
            name='snippet_grouper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='djangocms_snippet.SnippetGrouper'),
        ),
        migrations.AlterField(
            model_name='snippetptr',
            name='snippet_grouper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_snippet.SnippetGrouper'),
        ),
    ]
