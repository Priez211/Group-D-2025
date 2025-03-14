
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
urlpatterns = [
    path('', include('aits.urls')),
    path('admin/', admin.site.urls),
]
