# Generated by Django 4.1.3 on 2022-11-16 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0006_bookinstance_reader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=tinymce.models.HTMLField(verbose_name='summary'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='reader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taken_books', to=settings.AUTH_USER_MODEL, verbose_name='reader'),
        ),
    ]
