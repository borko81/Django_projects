# Импортват се стандартни модули
from django.http import Http404
from django.shortcuts import render
from django.db.models import Sum, Count

# Основно ще ползвам APIView, защото има повече възможност за контрол на правилата, за сметка на малкото писане!
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# За да се връща по-приветлив статус се импортва status
from rest_framework import status

# Импорт на модулите за аутентикация...
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# От лекцията.
from .permissions import IsOwnerOrReadOnly

# Добавят се моделите и сериализаторите, които са зададени
from .models import Groups, ElementIntown, Elements, StoreTown
from .serializers import ElementsSerializer, elementsInTownSerializer, TownSerializer, UserSerializer, elementsInTownSerializerOutUser, BasicGroupSerializer, FullGroupSerializer


# КЛAСОВЕTE
#-------------------------------------------------------------------------------------------------
class UserCreate(APIView):
    """
        Клас за създаване на потребител, само пост! Очакван модел:
        {"username": "Djano", "email": "potrebitel@abv.bg", "password": "django123"}
    """
    #serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------------------------------------------------------------


class GroupList(APIView):
    """
    Листва елементите от модел Групи
    Oчаквана форма: {"name" : "Група 2", "vip": 1}
    """
    permission_classes = (permissions.IsAuthenticated, )
    # Това нямам идея защо се добавя, но без него нямам html_form и raw_input!!!!!!
    serializer_class = FullGroupSerializer

    def get(self, request, format=None):
        select = Groups.objects.all()
        serializer = BasicGroupSerializer(select, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FullGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------------------------------------------------------------


class GroupsDetail(APIView):
    """
    Листва детаилна информация за групите от въведено id.
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = FullGroupSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува групата """
        try:
            return Groups.objects.get(pk=pk)
        except Groups.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за група """
        select = self.get_objects(pk)
        serializer = FullGroupSerializer(select)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Променя детаилите на група """
        select = self.get_objects(pk)
        serializer = FullGroupSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Пачва детаилите на група
            пачва се само името в случая, защото е свързано с FK!
        """
        select = self.get_objects(pk)
        serializer = FullGroupSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Трие група през id-то """
        select = self.get_objects(pk)
        select.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Класовете на елементите------------------------------------------------------------------------------
class ElementList(APIView):
    """
    Листва елементите от модел Елементи
    Oчаквана форма: {"name": "Елемент 1", "info": "Хубав Елемент", "price": 1.11, "group_name": 1}
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ElementsSerializer

    def get(self, request, format=None):
        select = Elements.objects.all()
        serializer = ElementsSerializer(select, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Информативен view с цел да покаже само елемените от търсена група---------------------------------------
class ElementListByGroup(APIView):
    """
    Листва елементите от модел Елементи по зададена група
    правата са зададени на "IsAuthenticatedOrReadOnly" с идеята, че потребител може да вижда информацията
    дори да не е регистриран.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ElementsSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува елемента """
        try:
            return Elements.objects.filter(group_name=pk)
            # return Elements.objects.filter(group_name=pk).aggregate(Sum('price'))
        except Elements.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за елемента """
        select = self.get_objects(pk)
        serializer = ElementsSerializer(select, many=True)
        return Response(serializer.data)


# Информативен view с цел да покаже сумата на елементите в избраната група---------------------------
class ElementSumByGroup(APIView):
    """
    Показва каква е общата стойност (сума) на елементите в избраната категория,
    броя елементи в избранта група и средната пара на елемент.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ElementsSerializer

    def get(self, request, pk, format=None):
        """ Взема брои и сума  на елементите """
        units = Elements.objects.filter(group_name=pk).aggregate(Count('price'))
        suma = Elements.objects.filter(group_name=pk).aggregate(Sum('price'))
        average = suma["price__sum"] / units["price__count"]
        total = {
            'units': units,
            'suma': suma,
            'average_price': average,
        }
        return Response(total)


# Kлас view връщащ детайлна информация за продукта-------------------------------------------------------
class ElementListDetail(APIView):
    """
    Листва детайлна информация за елемента от въведено id (primary key).
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ElementsSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува елемента """
        try:
            return Elements.objects.get(pk=pk)
        except Elements.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за елемента """
        select = self.get_objects(pk)
        serializer = ElementsSerializer(select)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Променя детаилите на елемента """
        select = self.get_objects(pk)
        serializer = ElementsSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Пачва детаилите на елементите
        """
        select = self.get_objects(pk)
        serializer = ElementsSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Трие елемета през id-то """
        select = self.get_objects(pk)
        select.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Класовете на Градовете------------------------------------------------------------------------
class TownList(APIView):
    """
    Листва елементите от модел Градове
    Oчаквана форма: {"storename": "Велинград"}
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TownSerializer

    def get(self, request, format=None):
        select = StoreTown.objects.all()
        serializer = TownSerializer(select, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TownSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Клас ползващ се за детаилите на зададен град -----------------------------------------------------
class TownListDetail(APIView):
    """
    Листва детаилна информация за елемента от въведено id.
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TownSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува елемента """
        try:
            return StoreTown.objects.get(pk=pk)
        except StoreTown.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за елемента """
        select = self.get_objects(pk)
        serializer = TownSerializer(select)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Променя детаилите на елемента """
        select = self.get_objects(pk)
        serializer = TownSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Пачва детаилите на градовете
        """
        select = self.get_objects(pk)
        serializer = TownSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Трие елемета през id-то """
        select = self.get_objects(pk)
        select.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Класовете на Елементите по градове----------------------------------------------------------

class elementsInTownList(APIView):
    """
    Листва елементите от модел Елементи по градове
    Oчаквана форма: {"store": 1, "elem": [1]}
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = elementsInTownSerializer

    def get(self, request, format=None):
        select = ElementIntown.objects.all()
        serializer = elementsInTownSerializer(select, many=True)
        result = serializer.data
        return Response(result,
                        status=status.HTTP_200_OK
                        )

    def post(self, request, format=None):
        serializer = elementsInTownSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------------------------------------------
class elementsInTownDetail(APIView):
    """
    Листва детаилна информация за елемента от въведено id.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = elementsInTownSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува елемента """
        try:
            return ElementIntown.objects.get(pk=pk)
        except ElementIntown.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за елемента """
        select = self.get_objects(pk)
        serializer = elementsInTownSerializer(select)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Променя детаилите на елемента """
        select = self.get_objects(pk)
        serializer = elementsInTownSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Пачва детаилите на градовете
        """
        select = self.get_objects(pk)
        serializer = elementsInTownSerializer(instance=select, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Трие елемета през id-то """
        select = self.get_objects(pk)
        select.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --Elementi po grupi------------------------------------------------------------------------------------------
class elementsInTownOrderByTown(APIView):
    """
    Групира (показва) само елементите от зададен град.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = elementsInTownSerializer

    def get_objects(self, pk):
        """ Ще провери дали съществува елемента """
        try:
            return ElementIntown.objects.filter(store_details=pk)
        except ElementIntown.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Взема детаилите за елемента """
        select = self.get_objects(pk)
        serializer = elementsInTownSerializer(select, many=True)
        return Response(serializer.data)


# Филтер по грaдове.----------------------------------------------------------------------------------

class FiterREsult(APIView):
    """ Връща детаилите по избрано ид на град,
        ако потребителя не е логнат няма да вижда id_то.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            """ Функцията ще върне какви елементи има в избраният град """
            select = ElementIntown.objects.filter(store=pk)
            serializer = elementsInTownSerializer(select, many=True)
            return Response(serializer.data)
        else:
            """
                Функцията ще върне какви елементи има в избраният град
                без да покава id-ata.
            """
            select = ElementIntown.objects.filter(store=pk)
            serializer = elementsInTownSerializerOutUser(select, many=True)
            return Response(serializer.data)
