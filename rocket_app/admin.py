import nested_admin
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Element, Employee, Contact, Address, Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# class EmployeeInline(nested_admin.NestedStackedInline):
#     """
#     Class For Employee Inline View
#     """
#     model = Employee
#     fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_active')



class EmployeeInline(nested_admin.NestedStackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



class AddressSectionInline(nested_admin.NestedStackedInline):
    """
    Class For Address SectionInline View
    """
    model = Address


class ContactSectionInline(nested_admin.NestedStackedInline):
    """
    Class For Contact SectionInline View
    """
    model = Contact
    inlines = [AddressSectionInline]


class ElementAdmin(nested_admin.NestedModelAdmin):
    """
    Class For Element Admin View with Inlines
    """
    inlines = [
        EmployeeInline, ContactSectionInline
    ]
    model = Element


class EmployeeAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Employee, EmployeeAdmin)
