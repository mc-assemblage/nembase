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


def srafetch(cf):
	"""Read a file containing a list of NCBI SRA ids and retrieve the records in XML."""
	idlist = []
	reader = csv.reader(open(cf.get_input('resultlist'), 'rb'), quoting=csv.QUOTE_NONE)
	for row in reader:
		if len(row) > 0: idlist.append(row[0])

	root = None; tmp_root = None
	retmax = cf.get_parameter('retmax', 'int')
	for i in range(0, len(idlist), retmax):
 		params = {'db':'sra', 'id':','.join(idlist[i:i+retmax])}
 		cf.write_log("NCBISRAFetch: params: %s" % params)
 		data = getURL(EFETCH_URL, params)
 		try:
 			tmp_root = ElementTree.XML(data)
 		except ElementTree.ParseError:
 			cf.write_log("Received an invalid xml response: %s" % data)
 			return constants.GENERIC_ERROR
 		if not isinstance(root, ElementTree.Element):
 			root = tmp_root
 		else:
 			root.extend(tmp_root.getchildren())

	outfh = open(cf.get_output('srafetchxml'), 'w')
	if isinstance(root,ElementTree.Element):
		cf.write_log("NCBISRAFetch: retrieved %s records" % len(root.getchildren()))
		outfh.write(ElementTree.tostring(root))
	else:
		outfh.write("<?xml version=\"1.0\"?><No_results />")
	outfh.close()
	return constants.OK
anduril.main(srafetch)

	
	