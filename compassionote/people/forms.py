from django import forms
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms.models import formset_factory, modelformset_factory

import csv

from models import PersonData, ContactData, NameData, CsvUpload

"""class ContactQueryForm(ModelForm):
    class Meta:
        model = ContactData
        fields = ['id','fullName','fullTextAddress']
        
ContactQueryFormBase = modelformset_factory(ContactData, extra=0, fields = ('id','fullName','fullTextAddress'))

class ContactsFormSet(ContactQueryFormBase):
    def add_fields(self, form, index):
        super(ContactQueryFormBase, self).add_fields(form, index)
        form.fields['is_checked'] = forms.BooleanField(required=False)
        form.fields['somefield'].widget.attrs['class'] = 'somefieldclass'"""

class ImportForm(ModelForm):
    class Meta:
        model = CsvUpload
        fields = ['title', 'file', 'owner']
        
class PersonCreateForm(ModelForm):
    class Meta:
        model = PersonData
        fields = ['match', 'contact', 'pipl_id', 'search_pointer', 'created_by', 'owner']
        
class PersonUpdateForm(ModelForm):
    class Meta:
        model = PersonData
        fields = ['matched', 'contact', 'pipl_id', 'match', 'search_pointer', 'created_by', 'owner']
        
class PersonMatchForm(ModelForm):
    class Meta:
        model = PersonData
        fields = ['matched']