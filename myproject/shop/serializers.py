# Импортират се основни модули
from rest_framework import serializers

# От моделите се импортват таблиците с които ще се работи
from .models import Groups, Elements, StoreTown, ElementIntown

# Долното се добавя за да се използва регистрационната форма:
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
        Форма за регистрация, полетата които се попълват са:
        потребител, парола, emeil.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        """ Ако подадените данни са валидни се създава потребител """
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


# Сераилизатор на групите
def article_serializer_factory(choice="base"):
    class GroupsSerializer(serializers.ModelSerializer):
        """ Сериализиращ клас на групите връзката е към модел Groups """
        class Meta:
            model = Groups
            if choice == "base":
                fields = ['id', 'name']
                read_only_fields = ["id"]
            else:
                fields = ['id', 'name', "vip"]
                read_only_fields = ["id"]
    return GroupsSerializer


# Два модела базов без id и пълен с id
BasicGroupSerializer = article_serializer_factory(choice="base")
FullGroupSerializer = article_serializer_factory(choice="full")


class ElementsSerializer(serializers.ModelSerializer):
    """ Сериализиращ клас на елементите връзката е към модел Elements """

    group_details = serializers.ReadOnlyField(source='group_name.name')

    class Meta:
        model = Elements
        fields = ['id', 'name', "info", "price", 'group_name', 'group_details']


class TownSerializer(serializers.ModelSerializer):
    """ Сериализиращ клас на градовете връзката е към модел StoreTown """
    class Meta:
        model = StoreTown
        fields = ['id', 'storename']
        read_only_fields = ["id"]


class elementsInTownSerializer(serializers.ModelSerializer):
    """
        Сериализиращ клас на елемените в градове връзката е към модел ElementIntown
        ползват се две допълнителни обраборки, за да се покаже детаилите на градовете
        и детаилите на елементите.
    """

    elem_details = ElementsSerializer(source='elem', many=True, read_only=True)
    store_details = serializers.ReadOnlyField(source='store.get_store_info')

    class Meta:
        model = ElementIntown
        fields = ["id", "elem", "elem_details", "store_details", "store"]


class elementsInTownSerializerOutUser(serializers.ModelSerializer):

    store_name = serializers.ReadOnlyField(source='store.storename')

    class Meta:
        model = ElementIntown
        fields = ("elem", "store", 'store_name')
