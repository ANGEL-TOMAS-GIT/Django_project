"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('/home/')),
    path('home/', include('books.urls')),
    path('payments/', include('payments.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('books.api.urls', namespace='books_api')),
    path('api_cart/', include("books.cart.api.urls")),
    path('api_order/', include("books.orders.api.urls")),
    path('order/', include('books.orders.urls')),
    path('api-token-obtain/', obtain_auth_token, name='api=token-obtain'),
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL,
               document_root=settings.MEDIA_ROOT)
