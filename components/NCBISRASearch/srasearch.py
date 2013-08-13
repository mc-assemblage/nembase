from anduril import constants
from xml.etree import ElementTree
import anduril.main
import csv
import random
import time
import urllib
import urllib2


ESEARCH_URL="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"


def getURL(url, params={}):
	"""Submit a url request and return the response. This function implements a retry 
		mechanism if the request fails."""
	if params:
		url += urllib.urlencode(params)
	response = None
	while True:
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			break
		except urllib2.HTTPError:
			time.sleep(random.uniform(0, 0.5))
		except urllib2.URLError:
			time.sleep(random.uniform(1, 10))
	return response.read()


def srasearch(cf):
	term = cf.get_parameter("term", "string")
	params = {'db':'sra', 'term':term, 'usehistory':'y'}
	field = cf.get_parameter("field", "string")
	if field:
		params['field'] = field
	cf.write_log("NCBISRASearch: searching with params %s" % params)
	root = ElementTree.XML(getURL(ESEARCH_URL, params))
	result_count = root.findtext("Count")
	params['WebEnv'] = root.findtext("WebEnv")
	params['retstart'] = None
	params['retmax'] = cf.get_parameter("retmax", "int")
	outfh = open(cf.get_output("resultlist"), 'wb')
	writer = csv.writer(outfh, quoting=csv.QUOTE_NONE)
	for i in range(0, int(result_count), params['retmax']):
		params['retstart'] = str(i)
		root = ElementTree.XML(getURL(ESEARCH_URL, params))
		for idelement in root.findall("IdList/Id"):
			writer.writerow([idelement.text.strip()])
	outfh.close()
	return constants.OK
anduril.main(srasearch)



