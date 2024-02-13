"""
URL configuration for djangogramm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path
from django.views.generic import RedirectView

from main_app.forms import EmailAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/main_app/', permanent=True)),
    path('main_app/', include('main_app.urls')),

    # Подключение кастомной формы входа (EmailAuthenticationForm)
    path('accounts/login/', LoginView.as_view(authentication_form=EmailAuthenticationForm), name='login'),
    # Включение стандартных URL-шаблонов аутентификации Django
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
