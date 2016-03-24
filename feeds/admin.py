from django.contrib import admin
from .models import Feed, Author, Article

# Register your models here.
class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'last_fetch', 'is_active')
    list_filter = ('is_active', 'created', 'last_fetch')
    search_fields = ('title', 'url')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('last_fetch',)

admin.site.register(Feed, FeedAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ('created', 'updated')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Author, AuthorAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'feed', 'author', 'is_active')
    list_filter = ('published', 'is_active', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('feed', 'author')

admin.site.register(Article, ArticleAdmin)
