from django.contrib import admin
from .models import Banner, Category, Tag, Tui, Article, Link
# 导入需要管理的数据库表


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'tui', 'author', 'views', 'created_time']
    # 文章列表里显示想要显示的字段
    list_per_page = 10
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_info', 'img', 'link_url', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'index']
    list_per_page = 10


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'linkurl']
    list_per_page = 10


