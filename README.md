# README

---

A simple application that pulls thumbnails based on the Fedora API. This assumes that the content model includes a thumbnail datastream called 'TN'. It also works with pulling images from a 'JPG' datastream.

The images are saved to directory called **temp**.

#### Options

**Required**:

* user
* password
* and one of these two:
	* collection
	* itemName 

**About**:

* **user**: your fedora username
* **password**: your fedora password
* **location**: the URL for the fedora server (defaults to UTK Libraries production server if not specified)
* **itemName**: the PID of an object
* **output**: the name of your output file (only works with itemName. defaults to output.jpeg)
* **collection**: the namespace of a collection 
* **attempts**: the number of attempts to run against a collection (only works with collection--not itemName)
* **datastream**: defaults to thumbnail. specifying m will get a medium-size jpg instead

#### Examples

**Single File**

* python thumbnails.py -u username -p password -i adams%3A95 -o mynewthumb.jpeg

**Collection**

* python thumbnails.py -u username -p password -c adams -a 200