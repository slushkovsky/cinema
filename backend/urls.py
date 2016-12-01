from django.conf.urls import url
from django.contrib import admin

import demo.views as demo


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^/?$', demo.index)
]
