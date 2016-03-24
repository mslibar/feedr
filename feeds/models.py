from django.db import models

# Create your models here.
class ActiveEntry(models.Manager):
    def get_queryset(self):
        return super(ActiveEntry, self).get_queryset().filter(is_active=True)

class Feed(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    url = models.URLField(max_length=250, verbose_name="URL")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_fetch = models.DateTimeField(null=True)

    objects = models.Manager()
    active_feeds = ActiveEntry()

    class Meta:
        ordering = ['title']
        unique_together = ('title', 'url')

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    url = models.URLField(max_length=250, verbose_name="URL")
    published = models.DateTimeField()
    img_url = models.URLField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published_articles = ActiveEntry()

    class Meta:
        ordering = ['-published']
        unique_together = ('feed', 'url')

    def __str__(self):
        return self.title
