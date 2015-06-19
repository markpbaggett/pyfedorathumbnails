import requests
from PIL import Image
from StringIO import StringIO
from optparse import OptionParser

def singleThumb():
	global locationURL, userName, password, itemName, outputFile
	locationURL += itemName + '/datastreams/TN/content?download=true'
	r = requests.get(locationURL, auth=(userName, password))
	if r.status_code == 200:
		imageFile = StringIO(r.content)
		img = Image.open(imageFile)
		print 'Creating thumbnail for ' + itemName + ' as '+ outputFile + '. The format is ' + img.format + '.'
		img.save('temp/' + outputFile, "JPEG", quality=80, optimize=True, progressive=True)
	else:
		print 'Item does not exist.'
		
def collection(attempts):
	global locationURL, userName, password, itemName, outputFile
	i = 1
	totalObjects = 0
	while i < attempts:
		itemName = collectionName + '%3A' + `i`
		newUrl = locationURL + itemName + '/datastreams/TN/content?download=true'
		r = requests.get(newUrl, auth=(userName, password))
		if r.status_code == 200:
			imageFile = StringIO(r.content)
			img = Image.open(imageFile)
			img.save('temp/' + itemName + '.jpeg', "JPEG", quality=80, optimize=True, progressive=True)
			totalObjects += 1
		i += 1
	print 'Created %d thumbnails' % totalObjects

parser = OptionParser()
parser.add_option("-u", "--user", dest="userName", help="submit username")
parser.add_option("-p", "--password", dest="password", help="submit password")
parser.add_option("-l", "--location", dest="locationURL", help="specify URL")
parser.add_option("-i", "--itemName", dest="itemName", help="specify namespace of item")
parser.add_option("-o", "--output", dest="outputFile", help="specify outputFileName")
parser.add_option("-c", "--collection", dest="collectionName", help="specify a collection namespace")
parser.add_option("-a", "--attempts", dest="attempts", help="specify the last pid of a namespace")

(options, args) = parser.parse_args()
if options.userName is None or options.password is None:
    parser.print_help()
    parser.error("A username, password, and item is required!")
        
if options.collectionName and options.itemName:
    parser.print_help()
    parser.error("Can only specify a collection or a item--not both!")	

if options:
	userName = password = locationURL = itemName = outputFile = collectionName = ''
	attempts = 0
	if options.userName:
		userName = options.userName
	if options.password:
		password = options.password
	if options.locationURL:
		locationURL = options.locationURL
	else:
		locationURL = 'http://digital.lib.utk.edu:8080/fedora/objects/'
	if options.outputFile:
		outputFile = options.outputFile
	else:
		outputFile = 'output.jpeg'
	if options.attempts:
		attempts = int(options.attempts)
	else:
		attempts = 100
	if options.itemName:
		itemName = options.itemName
		singleThumb()
	if options.collectionName:
		collectionName = options.collectionName
		collection(attempts)