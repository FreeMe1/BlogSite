"""BlogSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views as B_views
from media import views as M_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', B_views.index),
    url(r'^login/$', B_views.login),
    url(r'^confirm-api/$', B_views.confirm),
    url(r'^get-tags-api/$', B_views.get_tags),
    url(r'^add-tag-api/$', B_views.add_tag),
    url(r'^delete-tag-api/$', B_views.delete_tag),
    url(r'^get-tag-article-api/$', B_views.get_tag_article),
    url(r'^add-article-api/$', B_views.add_article),
    url(r'^get-article-api/$', B_views.get_article),
    url(r'^index-get-article/$', B_views.index_get_article),
    url(r'^media/$', M_views.media),
]
