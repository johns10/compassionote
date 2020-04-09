import csv, json
from address import AddressParser, Address
#from pipl.search import SearchAPIRequest, SearchAPIResponse
#from piplapis.data import Person
#from piplapis.data.fields import Name, Address
from nameparser import HumanName

from .models import Person, Name

contacts = []

with open("import_test.csv") as f:
    rows = csv.DictReader(f)
    #check the dictionary we imported to make sure it includes all the keys we need to convert a full text address into its components
    for row in rows:
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
            row['salutation'] = ''
        if 'middleName' not in row:
            row['middleName'] = ''
        if 'lastName' not in row:
            row['lastName'] = ''
        if 'nameSuffix' not in row:
            row['nameSuffix'] = ''
        if 'firstName' not in row:
            row['firstName'] = ''
        if 'nickName' not in row:
            row['nickName'] = ''
        #parse the full text name and full text address into their components and add them to the row.  For each row, we are checking the destination value to ensure it is empty, as users my import component values instead of full text values.
        parsedName = HumanName(row['fullName'])
        ap = AddressParser()
        parsedAddress = ap.parse_address(row['fullTextAddress'])
        if not row['salutation']:
            row['salutation'] = parsedName.title
        if not row['firstName']:
            People.Name.first = parsedName.first
            #row['firstName'] = parsedName.first
        if not row['middleName']:
            row['middleName'] = parsedName.middle
        if not row['lastName']:
            row['lastName'] = parsedName.last
        if not row['nameSuffix']:
            row['nameSuffix'] = parsedName.suffix
        if not row['nickName']:
            row['nickName'] = parsedName.nickname
        if not row['streetPrefix']:
            row['streetPrefix'] = parsedAddress.street_prefix
        if not row['houseNumber']:
            row['houseNumber'] = parsedAddress.house_number
        if not row['streetName']:
            row['streetName'] = parsedAddress.street
        if not row['streetSuffix']:
            row['streetSuffix'] = parsedAddress.street_suffix
        if not row['apartment']:
            row['apartment'] = parsedAddress.apartment
        if not row['building']:
            row['building'] = parsedAddress.building
        if not row['city']:
            row['city'] = parsedAddress.city
        if not row['state']:
            row['state'] = parsedAddress.state
        if not row['zip']:
            row['zip'] = parsedAddress.zip
        #append the dictionary to the list.  We are using a list of dictionaries.
        #contacts.append(row)
        

"""for contact in contacts:
    #set the output file name to the full text contact name, for now.
    fileName = 'pipltest/' + contact['fullName'] + '.txt'
    #we create an instance of the person class and append the values for name and address to that instance.  We build our request from that and send it to the pipl API.
    person = Person()
    person.names.extend([Name(first=contact['firstName'], middle=contact['middleName'], last=contact['lastName'], display=contact['fullName'])])
    person.addresses.extend([Address(house=contact['houseNumber'], street=contact['streetName']+" "+contact['streetSuffix'],city=contact['city'], country="US", state=contact['state'], zip_code=contact['zip'])])
    request = SearchAPIRequest(person=person)
    response = request.send()
    #write each full text json response to the output file.  We do this for each contact.
    output = open(fileName, 'w')
    output.write(response)
    output.close()
    with open(fileName, 'r') as f:
        contactJson = json.loads(f.read())
    print(contact['fullName'], " complete")"""

