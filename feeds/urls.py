from django.conf.urls import url
from . import views

app_name = 'feeds'

urlpatterns = [
    url(r'^authors.json$', views.AuthorsListView.json_response, name='authors_list_json'),
    url(r'^feed/(?P<id>[0-9]+)/(?P<slug>[-\w]+)/$', views.FeedArticlesListView.as_view(), name='feed_article_list'),
    url(r'^author/(?P<id>[0-9]+)/(?P<slug>[-\w]+)/$', views.AuthorArticlesListView.as_view(), name='author_article_list'),
    url(r'^articles/?$', views.ArticleListView.as_view(), name='articles_list'),
    url(r'^authors/?$', views.AuthorsListView.as_view(), name='authors_list'),
    url(r'^feeds/?$', views.FeedListView.as_view(), name='feeds_list'),
    url(r'^$', views.HomePageView.as_view(), name='home'),
]
