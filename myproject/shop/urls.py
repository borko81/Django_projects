from django.urls import path

from shop import views

urlpatterns = [
    # Показва групите
    path('groups/', views.GroupList.as_view(), name="groups-list"),
    # Показва детаилите на групите
    path('groups/<int:pk>/', views.GroupsDetail.as_view(), name="groups-detail-view"),

    # Показва Елементите
    path('elements/', views.ElementList.as_view(), name="elements-list"),
    # Показва детаилите на избраният елемент
    path('elements/<int:pk>/', views.ElementListDetail.as_view(), name="elements-detail-view"),
    # Показва елемените по зададена група
    path('elements/order/group/<int:pk>/', views.ElementListByGroup.as_view(), name="show-elem-bygroup"),
    # Показва сумата като пари на елементите в избраната група
    path('elements/order/group/<int:pk>/profit/', views.ElementSumByGroup.as_view(), name="show-elem-price-bygroup"),

    # Показва Градовете
    path('towns/', views.TownList.as_view(), name="towns-list"),
    # Показва детаилите на избраният Град
    path('towns/<int:pk>/', views.TownListDetail.as_view(), name="towns-detail-list"),

    # Показва Елементите по Градове
    path('store/', views.elementsInTownList.as_view(), name="store-list"),
    # Показва детаилите на Елементите по градове
    path('store/<int:pk>/', views.elementsInTownDetail.as_view(), name="store-by-town"),
    path('store/name/<int:pk>/', views.FiterREsult.as_view(), name="detail-store-by-town"),
    # Показва какви продукти има в избран склад. TODO!!!
    path('store/order/name/<int:pk>/', views.elementsInTownOrderByTown.as_view()),
]
