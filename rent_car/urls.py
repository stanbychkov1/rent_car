from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rent_car import settings

handler404 = 'cars.errors.page_not_found'
handler500 = 'cars.errors.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.urls')),
    path('', include('cars.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

