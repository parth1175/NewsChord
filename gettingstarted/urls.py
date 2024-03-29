from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path('items/<str:newsSourceName>/', hello.views.render_items, name='source'),
    path("AboutUs/", hello.views.AboutUs_page),
    path("admin/", admin.site.urls),
    path('article_download', hello.views.article_download_modal, name = 'article_download')
]
