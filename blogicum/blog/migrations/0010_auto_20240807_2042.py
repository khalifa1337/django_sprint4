# Generated by Django 3.2.16 on 2024-08-07 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comment_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_at',), 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
