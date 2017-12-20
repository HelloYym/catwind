# Generated by Django 2.0 on 2017-12-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QualityNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('thread', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=50, null=True)),
                ('link', models.URLField(null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('created', models.CharField(max_length=50, null=True)),
                ('author', models.CharField(max_length=50, null=True)),
                ('view_cnt', models.CharField(max_length=10, null=True)),
                ('summary', models.TextField(null=True)),
                ('keywords', models.TextField(null=True)),
                ('content', models.TextField(null=True)),
                ('raw_content', models.TextField(null=True)),
                ('image_url', models.TextField(null=True)),
            ],
            options={
                'db_table': 'spider_quality_news',
            },
        ),
        migrations.AlterUniqueTogether(
            name='qualitynews',
            unique_together={('thread', 'category')},
        ),
    ]
