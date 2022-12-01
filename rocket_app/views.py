from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Element, Address, Product
from .forms import CityNameFilterForm
from .serializers import ElementSerializer, ProductSerializer


def show_admin_custom_page(request):
    """
    Show Admin Page With All Elements
    :param request: Request Object
    :return: Render View Page
    """
    context = {
        'data': Element.objects.all()
    }
    return render(request, 'admin_custom_page.html', context)


def clear_childrens_debt(childrens_id: list):
    """
    Clear Childrens Dedt Function
    :param childrens_id: List of Childrens ID
    :return:
    """
    for child in childrens_id:
        worker = Element.get_by_id(child)
        worker.clear_debt()


def filter_worker_by_city(address: list, element: Element):
    """
    Get Worker By Filtered Addresses
    :param address: Filtered list of Addresses
    :param element: Parent Element
    :return: Workers List
    """
    workers = []
    for addres in address:
        if addres.contact.worker.parent == element:
            workers.append(addres.contact.worker)
    return workers


def show_admin_element_custom_page(request, id):
    """
    Show Element Custom Page
    :param request: Request Object
    :param id: Parent Element ID
    :return: Render View Page
    """
    worker_child = Element.get_childrens_by_id(id)
    worker = Element.get_by_id(id)

    if request.method == 'POST':
        clear_childrens_debt(request.POST.getlist('childrens'))

    elif request.method == 'GET':
        name = request.GET.get('name')

        if name:
            worker_child = filter_worker_by_city(
                Address.objects.filter(city=name), worker)

    context = {
        'form': CityNameFilterForm(),
        'object': worker,
        'childrens': worker_child
    }
    return render(request, 'admin_element_custom_page.html', context)


class ElementAPIView(APIView):
    """
    API For Element
    """
    def get(self, request, *args, **kwargs):
        """
        GET Method
        :param request: Request Object
        :return: JSON
        """
        id = kwargs.get('id', None)
        if id:
            objects = Element.objects.filter(id=id).first()
            return Response({'objects': ElementSerializer(objects, many=False).data})
        else:
            objects = Element.objects.all()
            return Response({'objects': ElementSerializer(objects, many=True).data})

    def post(self, request):
        """
        POST Method
        :param request: Request Object
        :return: JSON
        """
        product_id = request.data['product_id']
        objects = Element.objects.filter(products=product_id)

        return Response({'objects': ElementSerializer(objects, many=True).data})

    def put(self, request, *args, **kwargs):
        """
        PUT Method
        :param reques: Request Object
        :param args: arguments
        :param kwargs: key-words arguments
        :return:
        """
        id = kwargs.get('id', None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Element.objects.get(id=id)
        except:
            return Response({"error": "Object does not exist"})

        serializer = ElementSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"element": serializer.data})

    def delete(self, request, *args, **kwargs):
        """
        Delete Element method
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        id = kwargs.get('id', None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})
        try:
            instance = Element.objects.get(id=id)
        except:
            return Response({"error": "Object does not exist"})

        instance.delete()
        return Response({"status": "ok"})


class ProductAPIView(APIView):
    """
    API for Product
    """
    def get(self, request, *args, **kwargs):
        """
        GET Method
        :param request: Request Object
        :return: JSON
        """
        id = kwargs.get('id', None)
        if id:
            objects = Product.objects.filter(id=id).first()
            return Response({'objects': ProductSerializer(objects, many=False).data})
        else:
            objects = Product.objects.all()
            return Response({'objects': ProductSerializer(objects, many=True).data})

    def put(self, request, *args, **kwargs):
        """
        PUT Method
        :param reques: Request Object
        :param args: arguments
        :param kwargs: key-words arguments
        :return:
        """
        id = kwargs.get('id', None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Product.objects.get(id=id)
        except:
            return Response({"error": "Object does not exist"})

        serializer = ProductSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"element": serializer.data})

    def delete(self, request, *args, **kwargs):
        """
        Delete Product method
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        id = kwargs.get('id', None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})
        try:
            instance = Product.objects.get(id=id)
        except:
            return Response({"error": "Object does not exist"})

        instance.delete()
        return Response({"status": "ok"})


class CountryElementsAPIView(APIView):
    """
    API View For Elements From Country
    """
    def get(self, request):
        country = request.data['country']
        addresses = Address.objects.filter(country=country)
        elements = []

        for address in addresses:
            elements.append(address.contact.worker)

        return Response({'objects': ElementSerializer(elements, many=True).data})


class AvgDebtElementAPIView(APIView):
    """
    API View For Elements with Debt > Average Debt
    """
    def get(self, request):
        """
        GET Method
        :param request: Request Object
        :return: JSON
        """
        elements = []
        objects = Element.objects.all()
        avg_debt = Element.get_avg_debt()

        for object_ in objects:
            if object_.debt > avg_debt:
                elements.append(object_)

        return Response({'objects': ElementSerializer(elements, many=True).data})


class AddElementAPIView(APIView):
    """
    API View For Adding Element
    """
    def post(self, request):
        """
        POST method
        :param request: Request Object
        :return: JSON with Element Data
        """
        serializer = ElementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'element': serializer.data})
