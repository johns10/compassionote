from people.models import PersonData, NameData, EmailData, PhoneData, GenderData, EthnicityData, DobData, LanguageData, AddressData, RelationshipData, UserIdData, UrlData, ContactData, CsvUpload, Group, User
from guardian.shortcuts import assign_perm
from requests import *

contacts = ContactData.objects.all()
people = PersonData.objects.all()
user = User.objects.get(pk=5)
group = Group.objects.get(pk=2)
for contact in contacts:
    contact.created_by = user
    contact.owner = group
    contact.save()
    assign_perm('view_contactdata', group, contact)
    assign_perm('view_contactdata', user, contact)
    assign_perm('change_contactdata', user, contact)
    assign_perm('delete_contactdata', user, contact)
for person in people:
    person.created_by = user
    person.owner = group
    person.save()
    assign_perm('view_persondata', group, person)
    assign_perm('view_persondata', user, person)
    assign_perm('change_persondata', user, person)
    assign_perm('delete_persondata', user, person)
    