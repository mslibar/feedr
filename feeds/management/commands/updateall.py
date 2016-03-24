from django.core.management.base import BaseCommand
from feeds.models import Feed, Author, Article
from django.template.defaultfilters import slugify
from django.utils import timezone
from datetime import datetime

import feedparser

def convertToDatetime(string):
    INPUT_FORMATS = [
        '%a, %d %b %Y %H:%M:%S %z',         #Sun, 20 Mar 2016 16:35:00 +0000
        '%a, %d %b %Y %H:%M:%S %Z'          #Tue, 22 Mar 2016 14:56:57 GMT
    ]

    for input_format in INPUT_FORMATS:
        try:
            date_object = datetime.strptime(string, input_format)
        except ValueError:
            date_object = timezone.now()

    return date_object

class Command(BaseCommand):
    help = 'Fetch all active feeds!'

    def handle(self, *args, **options):
        print('Started fetching feeds...')

        success = error = skip = 0

        feeds = Feed.active_feeds.all()

        for feed in feeds:
            print('Fetching articles from "{0}"...'.format(feed.title))

            entries = feedparser.parse(feed.url)

            for entry in entries['items']:
                print('Fetching "{0}"...'.format(entry.title))

                if not hasattr(entry, 'author'):
                    entry.author = feed.title
                elif not entry.author:
                    entry.author = feed.title

                try:
                    author_obj = Author.objects.get(name=entry.author, slug=slugify(entry.author))
                except Author.DoesNotExist:
                    author_obj = Author(name=entry.author, slug=slugify(entry.author))
                    author_obj.save()

                entry_img_url = ''

                if 'enclosures' in entry:
                    for enclosure in entry.enclosures:
                        if enclosure.type == 'image/jpeg':
                            entry_img_url = enclosure.href
                        elif enclosure.href.endswith('.jpg'):
                            entry_img_url = enclosure.href
                elif 'links' in entry:
                    for link in entry.links:
                        if link.type == 'image/jpg':
                            entry_img_url = link.href

                try:
                    article_obj = Article.objects.get(url=entry.link)
                    skip += 1
                    print('SKIPPED! "{0}" skipped.'.format(entry.title))
                except Article.DoesNotExist:
                    article_obj =  Article(
                        feed = feed,
                        title = entry.get('title', ''),
                        slug = slugify(entry.get('title', '')),
                        url = entry.get('link', ''),
                        published = entry.get('published', timezone.now()),
                        img_url = entry_img_url,
                        author = author_obj
                    )

                    if not isinstance(article_obj.published, datetime):
                        article_obj.published = convertToDatetime(article_obj.published)

                    try:
                        article_obj.save()
                        success += 1
                        print('SUCCESS! "{0}" successfully inserted.'.format(entry.title))
                    except:
                        error += 1
                        print('WARNING! There was a problem inserting "{0}"!'.format(entry.title))

        return 'SUMMARY: Inserted ({0}), Warning ({1}), Skipped ({2}).'.format(int(success), int(error), int(skip))
