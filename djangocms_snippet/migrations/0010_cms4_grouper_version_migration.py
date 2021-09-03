import logging
import settings

from django.db import migrations

# TODO: Remove this
from djangocms_versioning.constants import DRAFT

logger = logging.getLogger(__name__)


def cms4_grouper_version_migration(apps, schema_editor):
    grouper_count = 0
    version_count = 0

    ContentType = apps.get_model("contenttypes", "ContentType")
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SnippetGrouper = apps.get_model("djangocms_snippet", "SnippetGrouper")
    User = apps.get_model('auth', 'User')
    Version = apps.get_model("djangocms_versioning", "Version")

    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')
    snippet_queryset = Snippet.objects.all()

    for snippet in snippet_queryset:
        grouper = SnippetGrouper.objects.create()
        snippet.new_snippet = grouper
        snippet.save()
        logger.info(f"Created Snippet Grouper ID: {snippet.snippet_grouper}")
        grouper_count += 1

        # Get a migration user.
        # TODO: Use environment variable, fall back to setting, then to default
        migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
        if not migration_user:
            logger.warning(
                "Setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID not provided, defaulting to user id: 1"
            )
            migration_user = User.objects.get(id=1)

        version = Version.objects.create(
            created_by=migration_user,
            state=DRAFT,
            number=1,
            object_id=snippet.pk,
            content_type=snippet_contenttype,
        )
        logger.info(f"Created Snippet Version ID: {version.pk}")
        # This will be necessary when versioning checks are implemented
        version_count += 1

    logger.info(f"Migration created {grouper_count} SnippetGrouper models and {version_count} Version models")


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0009_auto_20210831_0715'),
    ]

    operations = [
        migrations.RunPython(cms4_grouper_version_migration)
    ]
