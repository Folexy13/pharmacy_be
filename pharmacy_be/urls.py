from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supplements/', include('supplements.urls')),  # Ensure this is correctly pointing to your app's urls.py
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
