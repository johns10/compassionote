import csv
import itertools

from address import AddressParser, Address
from nameparser import HumanName

from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import Max
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView, ProcessFormView

from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import get_objects_for_user

import json
from pipl.search import SearchAPIRequest, SearchAPIResponse
from piplapis.data import Person
from piplapis.data.fields import Name, Address

from .forms import ImportForm, PersonCreateForm, PersonUpdateForm, PersonMatchForm
from .models import PersonData, NameData, EmailData, PhoneData, GenderData, EthnicityData, DobData, LanguageData, AddressData, RelationshipData, UserIdData, UrlData, ContactData, CsvUpload, Group

def index(request):
    return HttpResponse("Hello World!")
    
class ContactsListView(ListView):
    model = ContactData
    
    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        contacts = get_objects_for_user(self.request.user, 'people.view_contactdata')
        total = 0
        length = 0
        for contact in contacts:
            match = PersonData.objects.filter(contact_id=contact.id).aggregate(Max('match'))['match__max']
            if match == None:
                contact.match = "Not Matched"
            elif match != None:
                contact.match= str(PersonData.objects.filter(contact_id=contact.id).aggregate(Max('match'))['match__max']*100)+'%'
                total = total + match
                length = length + 1
        if (length >= 1):
            context['total_average'] = int((total/length)*100)
        else:
            context['total_average'] = 0
        context['object_list'] = contacts
        return context
    
class ContactCreate(PermissionRequiredMixin, CreateView):
    permission_required ='people.add_contactdata'
    model = ContactData
    fields = ['fullName', 'salutation', 'firstName', 'middleName', 'lastName', 'nameSuffix', 'nickName', 'fullTextAddress', 'streetPrefix', 'houseNumber', 'streetName', 'streetSuffix', 'apartment', 'building', 'city', 'state', 'zip', 'owner']
    
    #Workaround for this issue: https://github.com/django-guardian/django-guardian/issues/279
    def get_object(self):
        return None
        
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ContactCreate, self).form_valid(form)
                      
class ContactDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'people.view_contactdata'
    model = ContactData
    context_object_name = 'contact'

class ContactUpdate(PermissionRequiredMixin, UpdateView):
    permission_required ='people.change_contactdata'
    model = ContactData
    fields = ['fullName', 'salutation', 'firstName', 'middleName', 'lastName', 'nameSuffix', 'nickName', 'fullTextAddress', 'streetPrefix', 'houseNumber', 'streetName', 'streetSuffix', 'apartment', 'building', 'city', 'state', 'zip']   
    
class ContactDelete(PermissionRequiredMixin, DeleteView):
    permission_required ='people.delete_contactdata'
    model = ContactData
    success_url = reverse_lazy('contacts')
    
    #Workaround for this issue: https://github.com/django-guardian/django-guardian/issues/279
    def get_object(self):
        return None
    
    """def post(self, request, pk):
        #form = self.form_class(request.POST)
        matched = request.POST.getlist('matched')
        print request.POST
        print matched"""
    
#New importer view - doesn't currently work.  It needs to be hooked up to the form somehow
class CsvImportCreate(PermissionRequiredMixin, CreateView):
    permission_required ='people.add_contactdata'
    model = CsvUpload
    form_class = ImportForm
    
    #Workaround for this issue: https://github.com/django-guardian/django-guardian/issues/279
    def get_object(self):
        return None
            
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CsvImportCreate, self).form_valid(form)
        
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file')
            rows = csv.DictReader(file)
            for row in rows:
                if 'title' not in row:
                    row['title'] = ''
                if 'company' not in row:
                    row['company'] = ''
                if 'streetPrefix' not in row:
                    row['streetPrefix'] = ''
                if 'houseNumber' not in row:
                    row['houseNumber'] = ''
                if 'streetName' not in row:
                    row['streetName'] = ''
                if 'streetSuffix' not in row:
                    row['streetSuffix'] = ''
                if 'apartment' not in row:
                    row['apartment'] = ''
                if 'building' not in row:
                    row['building'] = ''
                if 'city' not in row:
                    row['city'] = ''
                if 'state' not in row:
                    row['state'] = ''
                if 'zip' not in row:
                    row['zip'] = ''
                if 'salutation' not in row:
                    row['salutation'] = ''
                if 'firstName' not in row:
                    row['firstName'] = ''
                if 'middleName' not in row:
                    row['middleName'] = ''
                if 'lastName' not in row:
                    row['lastName'] = ''
                if 'nameSuffix' not in row:
                    row['nameSuffix'] = ''
                if 'nickName' not in row:
                    row['nickName'] = ''
                input_data = ContactData()
                parsedName = HumanName(row['fullName'])
                ap = AddressParser()
                parsedAddress = ap.parse_address(row['fullTextAddress'])
                input_data.fullName = row['fullName']
                if not row['company']:
                    input_data.company = row['company']
                if not row['title']:
                    input_data.title = row['title']
                if not row['salutation']:
                    input_data.salutation = parsedName.title
                else:
                    input_data.salutation = row['title']
                if not row['firstName']:
                    input_data.firstName = parsedName.first
                else:
                    input_data.firstName = row['firstName']
                if not row['middleName']:
                    input_data.middleName = parsedName.middle
                else:
                    input_data.middleName = row['middleName']
                if not row['lastName']:
                    input_data.lastName = parsedName.last
                else:
                    input_data.lastName = row['lastName']
                if not row['nameSuffix']:
                    input_data.nameSuffix = parsedName.suffix
                else:
                    input_data.nameSuffix = row['nameSuffix']
                if not row['nickName']:
                    input_data.nickName = parsedName.nickname
                else:
                    input_data.nickName = row['nickName']
                input_data.fullTextAddress = row['fullTextAddress']
                if not row['streetPrefix']:
                    input_data.streetPrefix = parsedAddress.street_prefix
                else:
                    input_data.streetPrefix = row['streetPrefix']
                if not row['houseNumber']:
                    input_data.houseNumber = parsedAddress.house_number
                else:
                    input_data.houseNumber = row['houseNumber']
                if not row['streetName']:
                    input_data.streetName = parsedAddress.street
                else:
                    input_data.streetName = row['streetName']
                if not row['streetSuffix']:
                    input_data.streetSuffix = parsedAddress.street_suffix
                else:
                    input_data.streetSuffix = row['streetSuffix']
                if not row['apartment']:
                    input_data.apartment = parsedAddress.apartment
                else:
                    input_data.apartment = row['apartment']
                if not row['building']:
                    input_data.building = parsedAddress.building
                else:
                    input_data.building = row['building']
                if not row['city']:
                    input_data.city = parsedAddress.city
                else:
                    input_data.city = row['city']
                if not row['state']:
                    input_data.state = parsedAddress.state
                else:
                    input_data.state = row['state']
                if not row['zip']:
                    input_data.zip = parsedAddress.zip
                else:
                    input_data.zip = row['zip']
                input_data.created_by = self.request.user
                input_data.owner = Group.objects.get(pk=request.POST.get('owner'))
                input_data.save()
            return HttpResponseRedirect('/people/contacts/')
            
class PersonListView(ListView):
    model = PersonData
    
    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        people = get_objects_for_user(self.request.user, 'people.view_persondata')
        context['object_list'] = people
        return context
                  
class PersonDetailView(PermissionRequiredMixin, DetailView):
    permission_required ='people.view_persondata'    
    model = PersonData
    context_object_name = 'person'
    
    #def get_queryset(self):
    #    return PersonData.objects.all()
    
class PersonUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'people.change_persondata'
    model = PersonData
    context_object_name = 'person'
    form_class = PersonUpdateForm

#This is working but I need to improve performance    
class PersonMatch(PermissionRequiredMixin, UpdateView):
    permission_required = 'people.change_persondata'
    model = PersonData
    context_object_name = 'person'
    form_class = PersonMatchForm     
        
    def post(self, request, pk):
        form = self.form_class(request.POST)
        #print request.POST
        matched = request.POST.getlist('matched')
        redirect_pk = request.POST.get('contact')
        print redirect_pk
        pk = int(pk)
        if form.is_valid():
            if (matched):
                contact_id = request.POST.get('contact')
                people = PersonData.objects.filter(contact_id=contact_id)
                for person in people:
                    if (person.pk == pk):
                        person.matched = 1
                        person.save()
                    elif (person.pk != pk):
                        person.matched = 0
                        person.save()            
            return HttpResponseRedirect(reverse('people:contact-view', kwargs={'pk': redirect_pk}))#Better Implementation
                        
class PersonCreateView(PermissionRequiredMixin, CreateView):
    permission_required ='people.add_persondata'
    model = PersonData
    context_object_name = 'person'
    form_class = PersonCreateForm
    
    #Workaround for this issue: https://github.com/django-guardian/django-guardian/issues/279
    def get_object(self):
        return None
        
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PersonCreateView, self).form_valid(form)
        
    def post(self, request):
        form = self.form_class(request.POST)
        contactKeys = request.POST.getlist('contactKey')
        for contactKey in contactKeys:
            contact = ContactData.objects.get(pk=contactKey)
            person = Person()
            print"Processing ", contact.firstName, contact.lastName
            person.names.extend([Name(first=contact.firstName, middle=contact.middleName, last=contact.lastName, display=contact.fullName)])
            if contact.streetSuffix is not None:
                fullStreetName = contact.streetName+" "+contact.streetSuffix
            else:
                fullStreetName = contact.streetName
            person.addresses.extend([Address(house=contact.houseNumber, street=fullStreetName,city=contact.city, country="US", state=contact.state, zip_code=contact.zip)])#This needs to be modified to handle empty fields
            pipl_request = SearchAPIRequest(person=person)
            response = pipl_request.send()
            contactJson = json.loads(response)
            if 'person' in contactJson:
                matched = 1 #needs to be tested with this value set
                self.pipl_store(contact, contactJson['person'], request, matched)
            if 'possible_persons' in contactJson:
                for person in contactJson['possible_persons']:
                    matched = 0
                    self.pipl_store(contact, person, request, matched)
            matched = 0
        return HttpResponseRedirect('/people/contacts/')

    def pipl_store(self, contact, contactJson, request, matched):
        person_data = PersonData()
        if '@id' in contactJson:
            person_data.pipl_id = contactJson['@id']
        if '@match' in contactJson:
            person_data.match = contactJson['@match']
        person_data.created_by = self.request.user
        person_data.owner = contact.owner
        person_data.search_pointer = contactJson['@search_pointer']
        index = 0
        person_data.contact = contact
        person_data.save()
        if 'names' in contactJson:
            for name in contactJson['names']:
                name_data = NameData()
                name_data.person = person_data
                if '@valid_since' in name:
                    name_data.valid_since = name['@valid_since']
                if 'prefix' in name:
                    name_data.prefix = name['prefix']
                if 'first' in name:
                    name_data.first = name['first']
                if 'middle' in name:
                    name_data.middle = name['middle']
                if 'last' in name:
                    name_data.last = name['last']
                if 'display' in name:
                    name_data.display = name['display']        
                name_data.save()
        if 'emails' in contactJson:
            for email in contactJson['emails']:
                email_data = EmailData()
                email_data.person = person_data
                if '@valid_since' in email:
                    email_data.valid_since = email['@valid_since']
                if '@email_provider' in email:
                    email_data.email_provider = email['@email_provider']
                if 'address' in email:
                    email_data.email_address = email['address']
                if 'address_md5' in email:
                    email_data.email_address_md5 = email['address_md5']
                email_data.save()
        if 'phones' in contactJson:
            for phone in contactJson['phones']:
                phone_data = PhoneData()
                phone_data.person = person_data
                if '@valid_since' in phone:
                    phone_data.valid_since = phone['@valid_since']
                if '@type' in phone:
                    phone_data.type = phone['@type']
                if 'country_code' in phone:
                    phone_data.country_code = phone['country_code']
                if 'number' in phone:
                    phone_data.number = phone['number']
                if 'display' in phone:
                    phone_data.display = phone['display']
                if 'display_international' in phone:
                    phone_data.display_international = phone['display_international']
                phone_data.save()
        if 'gender' in contactJson:
            gender_data = GenderData()
            gender_data.person = person_data
            if '@valid_since' in contactJson['gender']:
                gender_data.valid_since = contactJson['gender']['@valid_since']
            if 'content' in contactJson['gender']:
                gender_data.content = contactJson['gender']['content']
            gender_data.save()
        if 'ethnicity' in contactJson:
            for ethnicity in contactJson['ethnicity']:
                ethnicity_data = EthnicityData()
                ethnicity_data.person = person_data
                if '@valid_since' in ethnicity:
                    ethnicity_data.valid_since = ethnicity['@valid_since']
                if 'content' in ethnicity:
                    ethnicity_data.content = ethnicity['content']
                ethnicity_data.save()
        if 'dob' in contactJson:
            dob = contactJson['dob']
            dob_data = DobData()
            dob_data.person = person_data
            if '@valid_since' in dob:
                dob_data.valid_since = dob['@valid_since']
            if 'display' in dob:
                dob_data.display = dob['display']
            if 'start' in dob['date_range']:
                dob_data.start = dob['date_range']['start']
            if 'end' in dob['date_range']:
                dob_data.end = dob['date_range']['end']
            dob_data.save()
        if 'languages' in contactJson:
            for language in contactJson['languages']:
                language_data = LanguageData()
                language_data.person = person_data
                if 'inferred' in language:
                    language_data.inferred = language['@inferred']
                if 'language' in language:
                    language_data.language = language['language']
                if 'region' in language:
                    language_data.region = language['region']
                if 'display' in language:
                    language_data.display = language['display']
                language_data.save()
        if 'addresses' in contactJson:
            for address in contactJson['addresses']:
                address_data = AddressData()
                address_data.person = person_data
                if '@valid_since' in address:
                    address_data.valid_since = address['@valid_since']
                if 'street_prefix' in address:
                    address_data.street_prefix = address['street_prefix']
                if 'house_number' in address:
                    address_data.house_number = address['house_number']
                if 'street_name' in address:
                    address_data.street_name = address['street_name']
                if 'street_suffix' in address:
                    address_data.street_suffix = address['street_suffix']
                if 'apartment' in address:
                    address_data.address = address['apartment']
                if 'building' in address:
                    address_data.building = address['building']
                if 'city' in address:
                    address_data.city = address['city']
                if 'state' in address:
                    address_data.state = address['state']
                if 'country' in address:
                    address_data.country = address['country']
                if 'zip' in address:
                    address_data.zip = address['zip']
                if 'display' in address:
                    address_data.display = address['display']
                address_data.save()
        """for relationship in contactJson['relatonships']:
            relationship_data = RelationshipData()
            if '@valid_since' in relationship:
                relationship_data.valid_since = relationship['@valid_since']
            if '"""
        if 'user_ids' in contactJson:
            for UserId in contactJson['user_ids']:
                userid_data = UserIdData()
                userid_data.person = person_data
                if '@valid_since' in UserId:
                    userid_data.valid_since = UserId['@valid_since']
                if 'content' in UserId:
                    userid_data.content = UserId['content']
                userid_data.save()
        if 'urls' in contactJson:
            for url in contactJson['urls']:
                url_data = UrlData()
                url_data.person = person_data
                if '@source_id' in url:
                    url_data.source_id = url['@source_id']
                if '@domain' in url:
                    url_data.domain = url['@domain']
                if '@name' in url:
                    url_data.name = url['@name']
                if '@category' in url:
                    url_data.name = url['@category']
                if 'url' in url:
                    url_data.url = url['url']
                url_data.save()
        return HttpResponseRedirect('/people/contacts/')
                    
#Old importer view
"""def CsvImportCreate(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/people/contacts/')
    else:
        form = ImportForm()
    return render(request, 'people/csvupload_form.html', {'form': form})"""
    
#Old ContactsListView that takes permissions into account, but is a function view instead of a generic view.
"""def ContactsListView(request, template_name='people/contactdata_list.html'):
    contacts = get_objects_for_user(request.user, 'people.view_contactdata')
    print contacts
    return render_to_response(template_name, {'object_list': contacts}, RequestContext(request))"""

#Old ContactsListView that doesn't take permissions into account
"""class ContactsListView(ListView):
    model = ContactData
    context_object_name = 'contacts'
    
    def get_queryset(self):
        return ContactData.objects.all()"""