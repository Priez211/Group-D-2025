from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aits.urls')),  # Include aits app URLs under /api/
    path('', include('aits.urls')),  # Include aits app URLs at root level
] 