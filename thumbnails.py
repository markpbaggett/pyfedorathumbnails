import requests
from PIL import Image
from StringIO import StringIO
from optparse import OptionParser

parser = OptionParser()
parser = OptionParser()
parser.add_option("-u", "--user", dest="userName", help="submit username")
parser.add_option("-p", "--password", dest="password", help="submit password")
parser.add_option("-l", "--location", dest="locationURL", help="specify URL")
parser.add_option("-i", "--itemName", dest="itemName", help="specify namespace of item")
parser.add_option("-o", "--output", dest="outputFile", help="specify outputFileName")

(options, args) = parser.parse_args()
if options.userName is None or options.password is None or options.itemName is None:
        parser.print_help()
        parser.error("A username, password, and item is required!")

if options:
	userName = password = locationURL = itemName = outputFile = ''
	if options.userName:
		userName = options.userName
	if options.password:
		password = options.password
	if options.locationURL:
		locationURL = options.locationURL
	else:
		locationURL = 'http://digital.lib.utk.edu:8080/fedora/objects/'
	if options.itemName:
		itemName = options.itemName
	if options.outputFile:
		outputFile = options.outputFile
	else:
		outputFile = 'output.jpeg'
	
locationURL += itemName + '/datastreams/TN/content?download=true'

r = requests.get(locationURL, auth=(userName, password))

imageFile = StringIO(r.content)
img = Image.open(imageFile)
print 'Creating thumbnail for ' + itemName + ' as '+ outputFile + '. The format is ' + img.format + '.'
img.save('temp/' + outputFile, "JPEG", quality=80, optimize=True, progressive=True)