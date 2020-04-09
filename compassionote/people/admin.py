from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import PersonData, NameData, AddressData, EmailData, PhoneData, GenderData, EthnicityData, DobData, LanguageData,  RelationshipData, UserIdData, UrlData, ContactData, CsvUpload

# Register your models here.

class NameInline(admin.StackedInline):
    model = NameData
    extra = 0
    
class EmailInline(admin.StackedInline):
    model = EmailData
    extra = 0
    
class PhoneInline(admin.StackedInline):
    model = PhoneData
    extra = 0
    
class GenderInline(admin.StackedInline):
    model = GenderData
    extra = 0
    
class EthnicityInline(admin.StackedInline):
    model = EthnicityData
    extra = 0

class DobInline(admin.StackedInline):
    model = DobData
    extra = 0
    
class LanguageInline(admin.StackedInline):
    model = LanguageData
    extra = 0
    
class AddressInline(admin.StackedInline):
    model = AddressData
    extra = 0
    
class RelationshipInline(admin.StackedInline):
    model = RelationshipData
    extra = 0
    
class UserIdInline(admin.StackedInline):
    model = UserIdData
    extra = 0
    
class UrlInline(admin.StackedInline):
    model = UrlData
    extra = 0

class PersonPermissionAdmin(GuardedModelAdmin):
    inlines = [NameInline, EmailInline, PhoneInline, GenderInline, EthnicityInline,  LanguageInline, AddressInline, RelationshipInline, UserIdInline, UrlInline]
        
class ContactPermissionAdmin(GuardedModelAdmin):
    prepopulated_field = {"slug": ("fullName",)}
    list_display = ('fullName', 'fullTextAddress')
    search_field = ('fullName')    
            
admin.site.register(PersonData, PersonPermissionAdmin)
admin.site.register(NameData)
admin.site.register(EmailData)
admin.site.register(PhoneData)
admin.site.register(GenderData)
admin.site.register(EthnicityData)
admin.site.register(DobData)
admin.site.register(LanguageData)
admin.site.register(AddressData)
admin.site.register(RelationshipData)
admin.site.register(UserIdData)
admin.site.register(ContactData, ContactPermissionAdmin)
admin.site.register(CsvUpload)
