from anduril import constants
from xml.etree import ElementTree
import anduril.main
import csv
import random
import time
import urllib
import urllib2


EFETCH_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"


def getURL(url, params={}):
	"""Submit a url request and return the response. This function implements a retry 
		mechanism if the request fails."""
	if params:
		url += urllib.urlencode(params)
	data = None
	while True:
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			data = response.read()
			break
		except urllib2.HTTPError:
			time.sleep(random.uniform(0, 0.5))
		except urllib2.URLError:
			time.sleep(random.uniform(1, 10))
		except httplib.BadStatusLine:
			time.sleep(random.uniform(1, 10))
		except httplib.IncompleteRead:
			time.sleep(random.uniform(1, 10))
	return data


def nucoreESTFetch(cf):
	"""Read a file containing a list of NCBI ids and retrieve the records."""
	idlist = []
	reader = csv.reader(open(cf.get_input('resultlist'), 'U'), quoting=csv.QUOTE_NONE)
	for row in reader:
		if len(row) > 0: idlist.append(row[0])

	retmax = cf.get_parameter('retmax', 'int')
	retmode = cf.get_parameter('retmode', 'string')
	rettype = cf.get_parameter('rettype', 'string')
	
	outfh = open(cf.get_output('nucoreestfetch'), 'w')
	for i in range(0, len(idlist), retmax):
	 	params = {'db':'nucest', 'id':','.join(idlist[i:i+retmax]), 'retmode':retmode, \
	 		'rettype':rettype}
	 	data = getURL(EFETCH_URL, params)
	 	outfh.write(data)
	outfh.close()
	return constants.OK
anduril.main(nucoreESTFetch)

	
	