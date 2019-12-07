
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [

    # Достъп до Админ Панел, променен е заради бутфорс.
    path('secure_admin/', admin.site.urls, name="admin-site"),
    # От апито
    path('', include('shop.urls')),
    # За регистрация, логин и деолументация
    path('', include('shop.auth_doc_folder.urls')),


]

# С добавянето на долното имаме възможност резултата да се покаже в json, html, посредством добавяне на префикс към url-a
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['html', 'json'])
