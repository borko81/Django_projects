from django.urls import path, include
from shop.views import UserCreate

# За вход в системата
from rest_framework.authtoken import views as fr_views

# За гнериране на схема на сайта:
from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(title="Схема на API")

# За генериране на swagger
from rest_framework_swagger.views import get_swagger_view
swagger_view = get_swagger_view(title='Swagger views API')

# За генериране на документацията
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    # Вход в системата от auth следва логин, логоут и т.н.
    path('auth/', include('rest_framework.urls'), name='rest_framework_login'),
    # Регистрация на нов потребител
    path('register/', UserCreate.as_view(), name='account-create'),
    # Това е за вход с токен (50 на 50 да го махна)
    path('auth-token/', fr_views.obtain_auth_token, name='get-auth-token'),

    # Документация на проекта
    path('', include_docs_urls(title='My API doc')),
    # Схема на сайта ползва се schema
    path('schema/', schema_view),
    # Схема на сайта ползва се swagger
    path('swagger/', swagger_view),
]
