from optparse import OptionParser
from xml.etree import ElementTree
import sys


usage = "usage: %prog [options] <srafetchxml>"
parser = OptionParser(usage=usage)


class SRARun:
	"""Class to store run information from an SRA fetch xml result."""
	def __init__(self, accession, exp_accession, library_strategy, library_source, \
		library_selection, is_paired, nominal_length, linkers, platform):
		self.accession = accession
		self.exp_accession = exp_accession
		self.library_strategy = library_strategy
		self.library_source = library_source
		self.library_selection = library_selection
		self.is_paired = is_paired
		self.nominal_length = nominal_length
		self.linkers = linkers
		self.platform = platform


class SRAXMLParser:
	"""Parse an SRA XML file returning an SRAExpPackage instance."""
	def parse(self, xmlfile):
		root = ElementTree.parse(xmlfile)
		experiments = self.__parse_experiments(root)
		runs = []
		for run_el in root.iter('RUN'):
			accession = run_el.get('accession')
			exp_accession = run_el.find('EXPERIMENT_REF').get('accession')
			args = [accession, exp_accession] + experiments[exp_accession]
			runs.append(SRARun(*args))
		return runs
		
	def parseFromString(self, xmlstr):
		root = ElementTree.XML(xmlstr)
		experiments = self.__parse_experiments(root)
		runs = []
		for run_el in root.iter('RUN'):
			accession = run_el.get('accession')
			exp_accession = run_el.find('EXPERIMENT_REF').get('accession')
			args = [accession, exp_accession] + experiments[exp_accession]
			runs.append(SRARun(*args))
		return runs
		
	def __parse_experiments(self, root):
		"""Return a dictionary of experiment information."""
		experiments = {}
		for exp in root.iter('EXPERIMENT'):
			accession = exp.get('accession')
			library_desc = exp.find('DESIGN/LIBRARY_DESCRIPTOR')
			library_strategy = library_desc.findtext('LIBRARY_STRATEGY')
			library_source = library_desc.findtext('LIBRARY_SOURCE')
			library_selection = library_desc.findtext('LIBRARY_SELECTION')
			is_paired = False
			nominal_length = None
			if library_desc.find('LIBRARY_LAYOUT/PAIRED') is not None:
				is_paired = True
				nominal_length = library_desc.find('LIBRARY_LAYOUT/PAIRED').get(\
					'NOMINAL_LENGTH')
			read_specs = exp.findall('DESIGN/SPOT_DESCRIPTOR/SPOT_DECODE_SPEC/READ_SPEC')
			linkers = []
			for read_spec in read_specs:
				if read_spec.findtext('READ_TYPE') == 'Linker':
					linkers.append(read_spec.findtext('EXPECTED_BASECALL_TABLE/BASECALL'))
			platform = None
			if exp.find('PLATFORM/LS454') is not None:
				platform = '454'
			elif exp.find('PLATFORM/ILLUMINA') is not None:
				platform = 'Illumina'
			experiments[accession] = [library_strategy, library_source, \
				library_selection, is_paired, nominal_length, linkers, platform]
		return experiments
		
		
if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 1:
		parser.print_help()
		sys.exit(2)
	sraxmlparser = SRAXMLParser()
	runs = sraxmlparser.parse(args[0])
	for run in runs:
		print vars(run)


