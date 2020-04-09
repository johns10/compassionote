import csv, json
from address import AddressParser, Address
import usaddress

string = "361 Farmington Avenue PO Box 17183"

contacts = []

ap = AddressParser()
parsedAddress = ap.parse_address(string)
print parsedAddress
print "Street Prefix: ", parsedAddress.street_prefix
print "House Number: ", parsedAddress.house_number
print "Street: ", parsedAddress.street
print "Street Suffix: ", parsedAddress.street_suffix
print "Apartment: ", parsedAddress.apartment
print "Building: ", parsedAddress.building
print "City: ", parsedAddress.city
print "State: ", parsedAddress.state
print "Zip: ", parsedAddress.zip

usa = usaddress.tag(string)
print type(usa)
print ap
print usa
