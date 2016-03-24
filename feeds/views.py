from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from .models import Feed, Author, Article
from .forms import FeedForm

import json

# Form for source/feed submission
class FeedFormView(FormView):
    form_class = FeedForm

    def feed_form(self):
        return FeedForm()

    def post(self, request, **kwargs):
        form = FeedForm(request.POST)
        if form.is_valid():
            new_feed = form.save(commit=False)
            new_feed.slug = slugify(new_feed.title)
            new_feed.save()
            self.object_list = self.get_queryset()
            return self.render_to_response(super(FeedFormView, self).get_context_data(**kwargs))
        else:
            self.object_list = self.get_queryset()
            return self.render_to_response(super(FeedFormView, self).get_context_data(**kwargs))

# Homepage View
class HomePageView(FeedFormView, ListView):
    queryset = Feed.active_feeds.all().order_by('title')
    template_name = 'feeds/homepage.html'

# Display all sources/feeds
class FeedListView(ListView):
    queryset = Feed.active_feeds.all().order_by('title')
    context_object_name = 'feeds'
    template_name = 'feeds/feed/feeds_list.html'

# Display all authors
class AuthorsListView(ListView):
    queryset = Author.objects.all().order_by('name')
    template_name = 'feeds/feed/authors_list.html'
    paginate_by = 20

    def json_response(request):
        if request.method == 'POST':
            authors = Author.objects.all().filter(name__contains=str(request.POST['search'])).order_by('name')
            data = [{
                "value": item.name,
                "name": item.name,
                "search": item.name,
                "url": "/author/{0}/{1}".format(item.id, item.slug)
            } for item in authors]
            return HttpResponse(json.dumps(data), content_type='application/json')

# Display all articles
class ArticleListView(ListView):
    queryset = Article.published_articles.all().order_by('-published')
    template_name = 'feeds/feed/article_list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def active_feeds(self):
        return Feed.active_feeds.all().order_by('title')

# Display articles from one source/feed
class FeedArticlesListView(ListView):
    template_name = 'feeds/feed/article_list.html'
    paginate_by = 20

    def active_feeds(self):
        return Feed.active_feeds.all().order_by('title')

    def get_queryset(self):
        self.feed = get_object_or_404(Feed, id=self.kwargs['id'])
        return Article.published_articles.filter(feed=self.feed).order_by('-published')

# Display articles from one author
class AuthorArticlesListView(ListView):
    template_name = 'feeds/feed/article_list.html'
    paginate_by = 20

    def active_feeds(self):
        return Feed.active_feeds.all().order_by('title')

    def get_queryset(self):
        self.author = get_object_or_404(Author, id=self.kwargs['id'])
        return Article.published_articles.filter(author=self.author).order_by('-published')
