from django.contrib import admin

from .models import Contact, CustomerUser, PortFolio


admin.site.register(PortFolio)


class PortFolioInline(admin.TabularInline):
    model = PortFolio
    extra = 1
    


class ContactInline(admin.StackedInline):
    model = Contact
    can_delete = False
    fk_name = "user"


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    inlines = [ContactInline, PortFolioInline]

    def get_full_display(self, request):
        return [field.name for field in self.model._meta.fields]