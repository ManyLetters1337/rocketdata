from decimal import Decimal
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey

TYPES = {
    ('Factory', 'Factory'),
    ('Distributor', 'Distributor'),
    ('Dealership', 'Dealership'),
    ('Retail Network', 'Retail Network'),
    ('Individual Entrepreneur', 'Individual Entrepreneur')
}


class Element(MPTTModel):
    """
    Network Element Class
    """
    type = models.CharField(max_length=50, choices=TYPES, default='Factory')
    title = models.CharField(max_length=50)
    debt = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[
        MinValueValidator(Decimal('0.00'))])
    creation_time = models.TimeField(auto_now_add=True)
    products = models.ManyToManyField('Product')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        """
        Overriding __str__ method
        :return: str
        """
        return self.type + " " + self.title

    @classmethod
    def get_by_id(cls, id: int):
        """
        Get Element by ID
        :return: Element
        """
        return Element.objects.get(id=id)

    @classmethod
    def get_childrens_by_id(cls, id: int):
        """
        Get Childrens for Element
        :return: List of Childrens Elements
        """
        element = Element.get_by_id(id)
        return element.get_children()

    def clear_debt(self):
        """
        Clear Element Debt
        :return: Decimal Debt
        """
        self.debt = Decimal('0.00')
        self.save()
        return self.debt

    @staticmethod
    def get_avg_debt():
        """
        Get Average Debt for all Elements
        :return: Decimal Average Debt
        """
        debt_sum = Decimal('0.00')
        for object in Element.objects.all():
            debt_sum += object.debt
        return debt_sum / Element.objects.all().count()


class Employee(models.Model):
    """
    User Class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker = models.ForeignKey(Element, related_name='employees', on_delete=models.CASCADE, null=True)

    def __str__(self):
        """
        Overriding __str__ method
        :return:
        """
        if self.user.first_name and self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username


class Contact(models.Model):
    """
    Contact Model
    """
    worker = models.ForeignKey(Element, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        """
        Overriding __str__ method
        :return: str
        """
        return self.email


class Address(models.Model):
    """
    Address Model
    """
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=50)   # Change to Choice Field
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.IntegerField(null=True, validators=[MinValueValidator(1)])

    def __str__(self):
        """
        Overriding __str__ method
        :return: str
        """
        if self.house_number:
            return self.country + ' ' + self.city + ' ' + self.street + ' ' + self.house_number.__str__()
        else:
            return self.country + ' ' + self.city + ' ' + self.street


class Product(models.Model):
    """
    Product Class
    """
    title = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    release_time = models.TimeField()

    def __str__(self):
        """
        Overriding __str__ method
        :return: str
        """
        return self.title + ' ' + self.model
