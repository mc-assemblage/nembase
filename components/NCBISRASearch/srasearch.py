from anduril.args import *
from xml.etree import ElementTree
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
	return response.read()


params = {'db':'sra', 'term':term, 'usehistory':'y'}
if field:
	params['field'] = field
write_log("NCBISRASearch: searching with params %s" % params)
root = ElementTree.XML(getURL(ESEARCH_URL, params))
result_count = root.findtext("Count")
params['WebEnv'] = root.findtext("WebEnv")
params['retstart'] = None
params['retmax'] = retmax
writer = csv.writer(open(resultlist, 'wb'), quoting=csv.QUOTE_NONE)
for i in range(0, int(result_count), retmax):
	params['retstart'] = str(i)
	root = ElementTree.XML(getURL(ESEARCH_URL, params))
	for idelement in root.findall("IdList/Id"):
		writer.writerow([idelement.text.strip()])


