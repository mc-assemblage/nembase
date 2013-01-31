from anduril.args import *
from xml.etree import ElementTree
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
	response = None
	while True:
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			break
		except urllib2.HTTPError:
			time.sleep(random.uniform(0, 0.5))
	return response.read()


idlist = []
reader = csv.reader(open(resultlist, 'rb'), quoting=csv.QUOTE_NONE)
for row in reader:
	if len(row) > 0: idlist.append(row[0])

root = None
for i in range(0, len(idlist), retmax):
 	params = {'db':'sra', 'id':','.join(idlist[i:i+retmax])}
 	write_log("NCBISRAFetch: params: %s" % params)
 	if not isinstance(root, ElementTree.Element):
 		root = ElementTree.XML(getURL(EFETCH_URL, params))
 	else:
 		tmp_root = ElementTree.XML(getURL(EFETCH_URL, params))
 		root.extend(tmp_root.getchildren())

outfh = open(srafetchxml, 'w')
if isinstance(root,ElementTree.Element):
	write_log("NCBISRAFetch: retrieved %s records" % len(root.getchildren()))
	outfh.write(ElementTree.tostring(root))
outfh.close()

	
	