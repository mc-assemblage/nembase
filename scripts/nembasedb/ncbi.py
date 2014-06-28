from sraxmlparser import SRAXMLParser
from xml.etree import ElementTree
import random
import time
import urllib
import urllib2


ESEARCH_URL="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
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
	

def getESTAccessions(orgname):
	"""Return a list of EST accessions for orgname."""
	term = "%s[Organism]" % orgname
	params = {'db':'nucest', 'term':term, 'usehistory':'y'}
	root = ElementTree.XML(getURL(ESEARCH_URL, params))
	result_count = root.findtext("Count")
	params['WebEnv'] = root.findtext("WebEnv")
	params['retstart'] = None
	params['retmax'] = 2000
	accessions = []
	for i in range(0, int(result_count), params['retmax']):
		params['retstart'] = str(i)
		root = ElementTree.XML(getURL(ESEARCH_URL, params))
		for idelement in root.findall("IdList/Id"):
			accessions.append(idelement.text.strip())
	return accessions


def getESTCount(orgname):
	"""Return the number of ESTs available for orgname."""
	term = "%s[Organism]" % orgname
	params = {'db':'nucest', 'term':term, 'usehistory':'y'}
	root = ElementTree.XML(getURL(ESEARCH_URL, params))
	result_count = root.findtext("Count")
	return int(result_count)
	
	
def getSRARuns(orgname, platform):
	"""Return a list of run accessions for an organism given a sequencing platform."""
	assert platform in ['454', 'Illumina']
	term = "%s[Organism] AND transcriptom*" % orgname
	search_params = {'db':'sra', 'term':term, 'usehistory':'y'}
	root = ElementTree.XML(getURL(ESEARCH_URL, search_params))
	result_count = root.findtext("Count")
	if int(result_count) == 0:
		return []
	search_params['WebEnv'] = root.findtext('WebEnv')
	search_params['retmax'] = 20
	runs = []
	sraxmlparser = SRAXMLParser()
	for i in range(0, int(result_count), search_params['retmax']):
		search_params['retstart'] = str(i)
		root = ElementTree.XML(getURL(ESEARCH_URL, search_params))
		idlist = []
		for idelement in root.findall('IdList/Id'):
			idlist.append(idelement.text.strip())
		fetch_params = {'db':'sra', 'id':','.join(idlist)}
		sraruns = sraxmlparser.parseFromString(getURL(EFETCH_URL, fetch_params))
		for srarun in sraruns:
			if srarun.platform == platform:
				runs.append(srarun)
	return runs
	
	
	