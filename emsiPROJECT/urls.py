from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static #this is needed for file and image upload
from django.conf import settings

import emsi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emsi.urls', namespace = 'emsi')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
