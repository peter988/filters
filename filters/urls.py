from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static
from main.views import search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_view ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)