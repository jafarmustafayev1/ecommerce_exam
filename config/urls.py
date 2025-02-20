from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('baton/', include('baton.urls')),
                  path('', include('ecommerce.urls')),
                  path('user/', include('user.urls')),
                  path('social-auth/',
                       include('social_django.urls', namespace='social')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
