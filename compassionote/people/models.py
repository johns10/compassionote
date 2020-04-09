from __future__ import unicode_literals
import datetime
import string

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from guardian.shortcuts import assign_perm

@python_2_unicode_compatible   
class ContactData(models.Model):
    company = models.CharField(max_length=64, blank=True, null=True)
    title = models.CharField(max_length=32, blank=True, null=True)
    fullName = models.CharField(max_length=256, blank=True, null=True)
    salutation = models.CharField(max_length=32, blank=True, null=True)
    firstName = models.CharField(max_length=32, blank=True, null=True)#Need to validate this field to disallow single letter names
    middleName = models.CharField(max_length=32, blank=True, null=True)
    lastName = models.CharField(max_length=32, blank=True, null=True)
    nameSuffix = models.CharField(max_length=32, blank=True, null=True)
    nickName = models.CharField(max_length=32, blank=True, null=True)
    fullTextAddress = models.CharField(max_length=256, blank=True, null=True)
    #Old Address Parser Fields
    streetPrefix = models.CharField(max_length=32, blank=True, null=True)
    houseNumber = models.CharField(max_length=32, blank=True, null=True)
    streetName = models.CharField(max_length=32, blank=True, null=True)
    streetSuffix = models.CharField(max_length=32, blank=True, null=True)
    apartment = models.CharField(max_length=32,blank=True, null=True)
    building = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    zip = models.CharField(max_length=10,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    """New usaddress Address Parser Fields"""
    """#address number
    AddressNumber = models.CharField(max_length=32, blank=True, null=True)
    #a modifier before an address number, e.g. 'Mile', '#'
    AddressNumberPrefix = models.CharField(max_length=32, blank=True, null=True)
    #a modifier after an address number, e.g 'B', '1/2'
    AddressNumberSuffix = models.CharField(max_length=32, blank=True, null=True)
    #the name of a building, e.g. 'Atlanta Financial Center'
    BuildingName = models.CharField(max_length=64, blank=True, null=True)
    #words indicating that an address is a corner, e.g. 'Junction', 'corner of'
    CornerOf = models.CharField(max_length=32, blank=True, null=True)
    #a conjunction connecting parts of an intersection, e.g. 'and', '&'
    IntersectionSeparator = models.CharField(max_length=8, blank=True, null=True)
    #the name of a landmark, e.g. 'Wrigley Field', 'Union Station'
    LandmarkName = models.CharField(max_length=64, blank=True, null=True)
    #a non-address component that doesn't refer to a recipient
    NotAddress = models.CharField(max_length=64, blank=True, null=True)
    #a type of occupancy within a building, e.g. 'Suite', 'Apt', 'Floor'
    OccupancyType = models.CharField(max_length=64, blank=True, null=True)
    #the identifier of an occupancy, often a number or letter
    OccupancyIdentifier = models.CharField(max_length=32, blank=True, null=True)
    #city
    PlaceName = models.CharField(max_length=32, blank=True, null=True)
    #a non-address recipient, e.g. the name of a person/organization
    Recipient = models.CharField(max_length=32, blank=True, null=True)
    #state
    StateName = models.CharField(max_length=32, blank=True, null=True)
    #street name, excluding type & direction
    StreetName = models.CharField(max_length=32, blank=True, null=True)
    #a direction before a street name, e.g. 'North', 'S'
    StreetNamePreDirectional = models.CharField(max_length=32, blank=True, null=True)
    #a modifier before a street name that is not a direction, e.g. 'Old'
    StreetNamePreModifier = models.CharField(max_length=32, blank=True, null=True)
    # a street type that comes before a street name, e.g. 'Route', 'Ave'
    StreetNamePreType = models.CharField(max_length=32, blank=True, null=True)
    #a direction after a street name, e.g. 'North', 'S'
    StreetNamePostDirectional = models.CharField(max_length=32, blank=True, null=True)
    #a modifier adter a street name, e.g. 'Ext'
    StreetNamePostModifier = models.CharField(max_length=32, blank=True, null=True)
    #a street type that comes after a street name, e.g. 'Avenue', 'Rd'
    StreetNamePostType = models.CharField(max_length=32, blank=True, null=True)
    #the name/identifier of a subaddress component
    SubaddressIdentifier = models.CharField(max_length=32, blank=True, null=True)
    #a level of detail in an address that is not an occupancy within a building, e.g. 'Building', 'Tower'
    SubaddressType = models.CharField(max_length=32, blank=True, null=True)
    #the identifier of a USPS box group, usually a number
    USPSBoxGroupID = models.CharField(max_length=32, blank=True, null=True)
    #a name for a group of USPS boxes, e.g. 'RR'
    USPSBoxGroupType = models.CharField(max_length=32, blank=True, null=True)
    #the identifier of a USPS box, usually a number
    USPSBoxID = models.CharField(max_length=32, blank=True, null=True)
    #a USPS box, e.g. 'P.O. Box'
    USPSBoxType = models.CharField(max_length=32, blank=True, null=True)
    #zip code
    ZipCode = models.CharField(max_length=32, blank=True, null=True)"""
    
    class Meta:
        permissions = (
            ("view_contactdata", "Can view contact data"),
        )
        
    def get_absolute_url(self):
        return reverse('people:contact-view', kwargs={'pk': self.pk})#Better Implementation
        
    def __str__(self):
        return unicode(self.fullName)

def contact_data_post_save(sender, instance, **kwargs):
    user = instance.created_by
    group = instance.owner
    #print group #Added this, because for some reason it allows the following line to complete successfully.
    assign_perm('view_contactdata', group, instance) #For some reason this line fails with "DoesNotExist: Permission matching query does not exist.
    assign_perm('view_contactdata', user, instance)
    assign_perm('change_contactdata', user, instance)
    assign_perm('delete_contactdata', user, instance)
        
post_save.connect(contact_data_post_save, sender=ContactData)
      
#Old post save signal processor.  It stopped working because of the name of the function for some reason.  However I decided to stop using this way because the @receiver decorator doesn't call out the function name explicitly.
"""@receiver(post_save, sender=ContactData)
def contact_data_post_save(sender, instance, **kwargs):
    print "Assigning Permissions"
    user = instance.created_by
    group = instance.owner
    assign_perm('view_contactdata', group, instance)
    assign_perm('view_contactdata', user, instance)
    assign_perm('change_contactdata', user, instance)
    assign_perm('delete_contactdata', user, instance)"""
    
class PersonData(models.Model):
    contact = models.ForeignKey(ContactData, on_delete=models.CASCADE, related_name='people')
    matched = models.BooleanField()
    pipl_id = models.CharField(max_length=64, blank=True, null=True)
    match = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True)
    search_pointer = models.CharField(max_length=8192, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        permissions = (
            ("view_persondata", "Can view person data"),
        )
        
    def get_absolute_url(self):
        return reverse('people:person', kwargs={'pk': self.pk})#Better Implementation
        
    def __str__(self):
        return str(self.id)

def person_data_post_save(sender, instance, **kwargs):
    user = instance.created_by
    group = instance.owner
    #print group #Added this, because for some reason it allows the following line to complete successfully.
    assign_perm('view_persondata', group, instance) #For some reason this line fails with "DoesNotExist: Permission matching query does not exist.
    assign_perm('view_persondata', user, instance)
    assign_perm('change_persondata', user, instance)
    assign_perm('delete_persondata', user, instance)
        
post_save.connect(person_data_post_save, sender=PersonData)
        
class NameData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='names')
    valid_since = models.DateField(blank=True, null=True)
    first = models.CharField(max_length=64, blank=True, null=True)
    middle = models.CharField(max_length=64, blank=True, null=True)
    last = models.CharField(max_length=64, blank=True, null=True)
    suffix = models.CharField(max_length=64, blank=True, null=True)
    display = models.CharField(max_length=256)
    
    class Meta:
        permissions = (
            ("view_namedata", "Can view name data"),
        )
        
    #def __str__(self):
    #    return self.display
    
class EmailData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='emails')
    valid_since = models.DateField(blank=True, null=True)
    email_provider = models.NullBooleanField(blank=True, null=True)
    email_address = models.EmailField()
    email_address_md5 = models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        permissions = (
            ("view_emaildata", "Can view email data"),
        )
        
    #def __str__(self):
    #    return self.email_address
    
class PhoneData(models.Model):
    PHONE_TYPE = (
        ('work_phone', 'Work Phone'),
        ('home_phone', 'Home Phone'),
        ('work_fax', 'Work Fax'),
        ('mobile', 'Mobile Phone'),
        ('home_fax', 'Home Fax'),
        ('pager', 'Pager'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='phone')
    valid_since = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=16, choices=PHONE_TYPE, blank=True, null=True)
    country_code = models.IntegerField(blank=True, null=True)
    number = models.IntegerField()
    display = models.CharField(max_length=32, blank=True, null=True)
    display_international = models.CharField(max_length=32, blank=True, null=True)
    
    class Meta:
        permissions = (
            ("view_phonedata", "Can view phone data"),
        )
        
    #def __str__(self):
    #    return self.display
    
class GenderData(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='gender')
    content = models.CharField(max_length=6, choices=GENDER)
    
    class Meta:
        permissions = (
            ("view_genderdata", "Can view gender data"),
        )
        
    #def __str__(self):
    #    return self.content
     
class EthnicityData(models.Model):
    ETHNICITY = (
        ('white', 'White'),
        ('black', 'Black'),
        ('american_indian', 'American Indian'),
        ('alaska_native', 'Alaskan Native'),
        ('chinese', 'Chinese'),
        ('filipino', 'Filipino'),
        ('other_asian', 'Other Asian'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
        ('vietnamese', 'Vietnamese'),
        ('native_hawaiian', 'Native Hawaiian'),
        ('guamanian', 'Guamanian'),
        ('chamorro', 'Chamorro'),
        ('samoan', 'Samoan'),
        ('other_pacific_islander', 'Other Pacific Islander'),
        ('other', 'Other'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='ethnicities')
    valid_since = models.DateField(blank=True, null=True)
    content = models.CharField(max_length=16, choices=ETHNICITY)
    
    class Meta:
        permissions = (
            ("view_ethnicitydata", "Can view ethnicity data"),
        )
        
    #def __str__(self):
    #    return self.ethnicity_data_text
     
class DobData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='dobs')
    valid_since = models.DateField(blank=True, null=True)
    display = models.CharField(max_length=32)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    
    class Meta:
        permissions = (
            ("view_dobdata", "Can view dob data"),
        )
        
    #def __str__(self):
    #    return self.dob_data_text

class LanguageData(models.Model):
    LANGUAGES = (
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    )
    REGION = (
        ('us', 'United States'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='languages')
    inferred = models.NullBooleanField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    region = models.CharField(max_length=2, choices=REGION, blank=True, null=True)
    display = models.CharField(max_length=16, blank=True, null=True)
    
    class Meta:
        permissions = (
            ("view_languagedata", "Can view language data"),
        )
        
    #def __str__(self):
    #    return self.language_data_text
    
class AddressData(models.Model):
    STATES = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )
    COUNTRIES = (
        ('us', 'United States'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='addresses')
    valid_since = models.DateField(blank=True, null=True)
    street_prefix = models.CharField(max_length=32, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=64)
    street_suffix = models.CharField(max_length=32)
    apartment = models.IntegerField(blank=True, null=True)
    building = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, choices=STATES)
    country = models.CharField(max_length=2, choices=COUNTRIES)
    zip = models.CharField(max_length=32)
    display = models.CharField(max_length=128)
    
    class Meta:
        permissions = (
            ("view_addressdata", "Can view address data"),
        )
        
    #def __str__(self):
    #    return self.address_data_text
    
class RelationshipData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='relationships')
    valid_since = models.DateField(null=True)
    first = models.CharField(max_length=64, blank=True, null=True)
    middle = models.CharField(max_length=64, blank=True, null=True)
    last = models.CharField(max_length=64, blank=True, null=True)
    display = models.CharField(max_length=128)
    
    class Meta:
        permissions = (
            ("view_relationshipdata", "Can view relationship data"),
        )
        
    def __str__(self):
        return self.relationship_data_text
    
class UserIdData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='userids')
    valid_since = models.DateField(blank=True, null=True)
    content = models.CharField(max_length=64)
    
    class Meta:
        permissions = (
            ("view_useriddata", "Can view user ID data"),
        )
        
    #def __str__(self):
    #    return self.userid_data_text
    
class ImagesData(models.Model):
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='images')
    valid_since = models.DateField(blank=True, null=True)
    url = models.URLField()
    thumbnain_token = models.CharField(max_length=256, blank=True, null=True)
    
class UrlData(models.Model):
    CATEGORY = (
        ('background_reports', 'Background Reports'),
        ('contact_details', 'Contact Details'), 
        ('email_addresses', 'Email Addresses'), 
        ('media', 'Media'), 
        ('personal_profiles', 'Personal Profiles'), 
        ('professional_and_business', 'Professional and Business'), 
        ('public_records', 'Public Records'), 
        ('publications', 'Publications'), 
        ('school_and_classmates', 'School and Classmates'), 
        ('web_pages', 'Web Pages'),
    )
    person = models.ForeignKey(PersonData, on_delete=models.CASCADE, related_name='urls')
    source_id = models.CharField(max_length=64, blank=True, null=True)
    domain = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    category = models.CharField(max_length=32, choices=CATEGORY, blank=True, null=True)
    url = models.URLField()
    
    class Meta:
        permissions = (
            ("view_urldata", "Can view URL data"),
        )
        
    #def __str__(self):
    #    return self.url_data_text

class CsvUpload(models.Model):
    title = models.CharField(max_length=32)
    file = models.FileField(upload_to='imports/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('people:contacts')#Better Implementation
    
    class Meta:
        permissions = (
            ("view_csvupload", "Can view CSV uploads"),
        )
        
    #def __str__(self):
    #    return self.csv_upload_text
    
@receiver(post_save, sender=CsvUpload)
def contact_post_save(sender, instance, **kwargs):
    user = instance.created_by
    group = instance.owner
    assign_perm('view_csvupload', group, instance)
    assign_perm('view_csvupload', user, instance)
    assign_perm('change_csvupload', user, instance)
    assign_perm('delete_csvupload', user, instance)