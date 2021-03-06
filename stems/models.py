from django.db import models


class Lolly(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def update_attr(self, uf=[], mf=[], item=None):
        if not item: return

        for k in uf:
            setattr(self, k, item.get(k))
        for k in mf:
            ori = getattr(self, k).encode('utf8').split('\001')
            now = item.get(k).split('\001')
            setattr(self, k, '\001'.join(ori + now))


class QualityNews(Lolly):
    thread = models.IntegerField(null=False)
    category = models.CharField(max_length=50, null=False)
    source = models.CharField(max_length=50, null=True)
    link = models.URLField(null=True)

    title = models.CharField(max_length=200, null=True)
    location = models.TextField(null=True)
    created = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    view_cnt = models.CharField(max_length=10, null=True)
    summary = models.TextField(null=True)
    keywords = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)

    class Meta:
        app_label = 'stems'
        db_table = 'spider_quality_news'
        unique_together = ('thread', 'category')
