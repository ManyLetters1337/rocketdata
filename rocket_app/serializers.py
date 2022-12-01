from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Element, Contact, Address, Employee, Product
from typing import Dict


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """
    contact_id = serializers.IntegerField()

    class Meta:
        model = Address
        fields = ('contact_id', 'country', 'city', 'street', 'house_number')
        read_only_fields = ('contact_id',)


class ContactSerializer(serializers.ModelSerializer):
    """
    Contact Serializer
    """
    id = serializers.IntegerField()
    address_set = AddressSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('id', 'email', 'address_set')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer
    """
    id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'model', 'release_time')
        read_only_fields = ('id',)


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'password')


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee Serializer
    """
    id = serializers.IntegerField()
    user = CurrentUserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user')
        read_only_fields = ('id',)


class ElementSerializer(serializers.ModelSerializer):
    """
    Element Serializer
    """
    contact_set = ContactSerializer(many=True, required=False)
    products = ProductSerializer(many=True, required=False)
    employees = EmployeeSerializer(many=True, required=False)

    class Meta:
        model = Element
        depth = 1
        fields = ('type', 'title', 'debt', 'creation_time', 'employees', 'products', 'contact_set')
        read_only_fields = ('debt',)

    def create_product(self, products_data: Dict):
        """
        Create Product
        :param products_data:
        :return:
        """
        for product_data in products_data:
            product = Product.objects.filter(id=product_data.get('id')).first()
            if not product:
                product = Product.objects.create(**product_data)

    def create_employee(self, employees_data: Dict, element: Element):
        """
        Create Employee
        :param element: Element Object
        :param employees_data: Dict with kwargs
        :return:
        """
        for employee_data in employees_data:
            user = User.objects.create_user(**(employee_data.get('user')))
            Employee.objects.create(user=user, worker=element)

    def create_contact(self, contacts_data: Dict, element: Element):
        """
        Create Contact
        :param element: Element Object
        :param contacts_data: Dict with kwargs
        :return:
        """
        for contact_data in contacts_data:
            address_data = contact_data.pop('address_set')
            contact = Contact.objects.create(worker=element, **contact_data)
            Address.objects.create(contact=contact, **(address_data[0]))

    def create(self, validated_data: Dict):
        """
        Create Element method
        :param validated_data:
        :return: Element Object
        """
        employees_data = validated_data.pop('employees')
        products_data = validated_data.pop('products')
        contact_data = validated_data.pop('contact_set')

        element = Element.objects.create(**validated_data)

        if products_data: self.create_product(products_data)

        if employees_data: self.create_employee(employees_data, element)

        if contact_data: self.create_contact(contact_data, element)

        return element

    def update_product(self, products_data: Dict):
        """
        Update Product
        :param products_data:
        :return:
        """
        for product_data in products_data:
            product_id = product_data.get('id', None)
            if product_id:
                product = Product.objects.get(id=product_id)
                product.title = product_data.get('title', product.title)
                product.model = product_data.get('model', product.model)
                product.release_time = product_data.get('release_time', product.release_time)
                product.save()

    def update_address(self, addresses_data: Dict):
        """
        Update Address method
        :param addresses_data: Dict with kwargs
        :return:
        """
        for address_data in addresses_data:
            address_id = address_data.get('contact_id', None)
            if address_id:
                address = Address.objects.get(contact_id=address_id)
                address.country = address_data.get('country', address.country)
                address.city = address_data.get('city', address.city)
                address.street = address_data.get('street', address.street)
                address.house_number = address_data.get('house_number', address.house_number)
                address.save()

    def update_contact(self, contacts_data: Dict):
        """
        Update Contact method
        :param contacts_data: Dict with kwargs
        :return:
        """
        for contact_data in contacts_data:
            contact_id = contact_data.get('id', None)
            if contact_id:
                contact = Contact.objects.get(id=contact_id)
                contact.email = contact_data.get('email', contact.email)
                contact.save()

                address_data = contact_data.get('address_set')
                if address_data:
                    self.update_address(address_data)

    def update_employees(self, employees_data):
        """
        Update Employee method
        :param employees_data:
        :return:
        """
        for employee_data in employees_data:
            employee_id = employee_data.get('id', None)
            if employee_id:
                employee = Employee.objects.get(id=employee_id)
                user_data = employee_data.get('user')
                user = User.objects.get(id=employee.user.id)
                user.username = user_data.get('username', user.username)
                user.email = user_data.get('email', user.email)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.is_active = user_data.get('is_active', user.is_active)
                user.save()
                employee.save()

    def update(self, instance, validated_data: Dict):
        """
        Update Element method
        :param instance: Element Instance
        :param validated_data: Validated Data
        :return: Element Instance
        """
        employees_data = validated_data.get('employees')
        products_data = validated_data.get('products')
        contact_data = validated_data.get('contact_set')

        instance.type = validated_data.get('type', instance.type)
        instance.title = validated_data.get('title', instance.title)
        instance.debt = validated_data.get('debt', instance.debt)
        instance.creation_time = validated_data.get('creation_time', instance.creation_time)
        instance.save()

        if products_data:
            self.update_product(products_data)

        if contact_data:
            self.update_contact(contact_data)

        if employees_data:
            self.update_employees(employees_data)

        return instance
