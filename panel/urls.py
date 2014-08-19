# coding=utf-8

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

urlpatterns = [
    url(r"^ingresar/$",
        "django.contrib.auth.views.login",
        name="login"
        ),
    url(r"^salir/$",
        "django.contrib.auth.views.logout_then_login",
        name="logout"
        ),
    url(r"^cambiar-contrasena/$",
        "django.contrib.auth.views.password_change",
        name="password_change"
        ),
    url(r"^contrasena-cambiada/$",
        "django.contrib.auth.views.password_change_done",
        name="password_change_done"
        ),
    url(r'^tickets/',
        include('tickets.urls', namespace='tickets')
        ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
