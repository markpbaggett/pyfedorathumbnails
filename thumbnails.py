import requests
from PIL import Image
from StringIO import StringIO
from optparse import OptionParser

def singleThumb():
	global locationURL
	locationURL += itemName + '/datastreams/' + datastream + '/content?download=true'
	r = requests.get(locationURL)
	if r.status_code == 200:
		imageFile = StringIO(r.content)
		img = Image.open(imageFile)
		print 'Creating thumbnail for ' + itemName + ' as '+ outputFile + '.'
		img.save('temp/' + outputFile, "JPEG", quality=80, optimize=True, progressive=True)
	else:
		print 'Item does not exist.'

def collection():
	global locationURL
	i = 1
	totalObjects = 0
	while i < attempts:
		itemName = collectionName + '%3A' + `i`
		newUrl = locationURL + itemName + '/datastreams/' + datastream + '/content?download=true'
		r = requests.get(newUrl)
		if r.status_code == 200:
			imageFile = StringIO(r.content)
			img = Image.open(imageFile)
			img.save('temp/' + itemName + '.jpeg', "JPEG", quality=80, optimize=True, progressive=True)
			totalObjects += 1
		i += 1
	print 'Created %d thumbnails' % totalObjects

parser = OptionParser()
parser.add_option("-l", "--location", dest="locationURL", help="specify URL of fedora server. defaults to UTK Libraries")
parser.add_option("-i", "--itemName", dest="itemName", help="specify namespace of item")
parser.add_option("-o", "--output", dest="outputFile", help="specify output filename. defaults to output.jpeg")
parser.add_option("-c", "--collection", dest="collectionName", help="specify a collection namespace")
parser.add_option("-a", "--attempts", dest="attempts", help="specify the last pid of a namespace")
parser.add_option("-d", "--datastream", dest="datastream", help="specify datastream. use t for thumbnail or m for medium. defaults to thumbnail.")

(options, args) = parser.parse_args()

if options.collectionName and options.itemName:
    parser.print_help()
    parser.error("Can only specify a collection or a item--not both! For more information, see the README.")

if options:
	userName = password = locationURL = itemName = outputFile = collectionName = datastream = ''
	attempts = 0
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
	if options.datastream == 'm':
		datastream = 'JPG'
	else:
		datastream = 'TN'
	if options.itemName:
		itemName = options.itemName
		singleThumb()
	if options.collectionName:
		collectionName = options.collectionName
		collection()