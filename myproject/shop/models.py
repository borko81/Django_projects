from django.db import models


class Groups(models.Model):
    """
        Ще се ползва за модел на групите:
        NAME: 'name'- името на групата,
        NAME: vip'  - дали групата е вип т.е. дали ще има намаление или не.
    """
    name = models.CharField(max_length=20, unique=True)
    vip = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
            Предефинира се метода save, за да може, имената да се запишат директно
            като capitalize (за подобър вид)
        """
        for field_name in ['name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Groups, self).save(*args, **kwargs)

    @property
    def get_group_info(self):
        return {
            "id": self.id,
            "name": self.storename
        }

    def __str__(self):
        return f"{self.name} / vip {self.vip}"


class Elements(models.Model):
    """
        Ще се ползва за модел на елементите:
        NAME: 'name'- името на елемента,
        NAME: info'  - някакъв допълнителен пояснителен текст към елемента.
        NAME: 'price'- цена на елемента,
        NAME: 'group'- външен ключ към групите,
    """
    name = models.CharField(max_length=20, unique=True)
    info = models.TextField()
    price = models.FloatField()
    group_name = models.ForeignKey(Groups, on_delete=models.CASCADE)

    @property
    def get_elem_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "price": self.price,
        }

    def save(self, *args, **kwargs):
        """
        Предефинира се метода save, за да може, имената да се запишат директно
        като capitalize (за подобър вид)
        """
        for field_name in ['name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Elements, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class StoreTown(models.Model):
    """
        Ще се ползва за модел на гравоете:
        NAME: 'name'- името на града,
    """
    storename = models.CharField(max_length=20, unique=True)

    @property
    def get_store_info(self):
        return {
            "id": self.id,
            "name": self.storename
        }

    def save(self, *args, **kwargs):
        """
        Предефинира се метода save, за да може, имената да се запишат директно
        като capitalize (за подобър вид)
        """
        for field_name in ['storename']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(StoreTown, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.storename}"


class ElementIntown(models.Model):
    """
        Ще се ползва за модел на елементите в градовете:
        външни ключове, към склад и елементи, related_name: връзка към поле (незнам дали ще го ползвам)
    """
    store = models.ForeignKey(StoreTown, on_delete=models.CASCADE)
    elem = models.ManyToManyField(Elements, related_name='element_details')

    def __str__(self):
        return f"{self.store}"
