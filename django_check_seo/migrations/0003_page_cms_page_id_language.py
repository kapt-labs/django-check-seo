# Generated manually for django_cms_model_keywords

from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [
        ("django_check_seo", "0002_keyword_page"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="path",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=500,
                null=True,
                unique=False,
                verbose_name="path",
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="cms_page_id",
            field=models.PositiveIntegerField(
                blank=True,
                db_index=True,
                null=True,
                verbose_name="CMS page id",
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="language",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="language"
            ),
        ),
        migrations.AddConstraint(
            model_name="page",
            constraint=models.UniqueConstraint(
                condition=Q(path__isnull=False) & ~Q(path=""),
                fields=("path",),
                name="dcs_unique_page_path_when_set",
            ),
        ),
        migrations.AddConstraint(
            model_name="page",
            constraint=models.UniqueConstraint(
                condition=Q(cms_page_id__isnull=False),
                fields=("cms_page_id", "language"),
                name="dcs_unique_cms_page_language",
            ),
        ),
    ]
