
#Provides utilities for parsing and writing fastq files.

import re


class FastqFormatError(Exception):
	pass


class FastqParser:
	def parse(self, fh):
		"""Generator method. Parse a fastq file yielding FastqRecord objects."""
		while True:
			header = fh.readline().strip()
			if not header: break
			if not header.startswith("@"):
				raise FastqFormatError("FormatError", \
					"Error parsing fastq header 1 %s" % header)
			seq = fh.readline().strip()
			header2 = fh.readline()
			if not header2.startswith("+"):
				raise FastqFormatError("FormatError", \
					"Error parsing fastq header 2 %s" % header2)
			qual = fh.readline().strip()
			yield FastqRecord(header[1:], seq, qual, parse_qualities=False)


class FastqRecord:
	"""Wrapper around a fastq record."""
	def __init__(self, header, sequence, quality_str, header2=None, parse_qualities=True):
		self.header = header
		self.sequence = sequence
		self.qualities = quality_str
		self.__qual_encoded = False
		if parse_qualities:
			self.qualities = self.parse_qualities(quality_str)
			self.__qual_encoded = True
		self.header2 = header2
		
	def parse_qualities(self, quality):
		#detect the qual-type
		sanger_int_quals_regexp = re.compile("(\d{1,2})")
		sanger_regexp = re.compile("[!\"#$%&'()*+,-.\/0123456789:]")
		#solexa_regexp = re.compile("\;<=>\?")
		#illumina_regexp = re.compile("JKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh")
		illumina_solexa_regexp = re.compile("[\;<=>\?JKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh]")
		if len(sanger_int_quals_regexp.findall(quality)) == len(self.sequence):
			#sanger integer qualities
			return map(int, sanger_int_quals_regexp.findall(quality))
		elif len(sanger_regexp.findall(quality)) > 0:
			#sanger ascii encoded qualities
			return map(lambda x: ord(x) - 33, quality)
		elif len(illumina_solexa_regexp.findall(quality)) > 0:
			#illumina or solexa ascii encoded qualities
			return map(lambda x: ord(x) - 64, quality)
		else:
			raise Exception("ValueError", "Unknown quality type %s" % quality)
			
	def getIlluminaStr(self):
		"""Return a string representation of this record with Illumina encoded 
			qualities."""
		header2 = ""
		if self.header2:
			header2 = self.header2
		encoded_quality_str = self.qualities
		if self.__qual_encoded:
			encoded_quality_str = map(lambda x: chr(x+64), self.qualities)
		result = "@%s\n%s\n+%s\n%s" % (self.header, self.sequence, header2, \
			encoded_quality_str)
		return result
		
	def __str__(self):
		header2 = ""
		if self.header2:
			header2 = self.header2
		encoded_quality_str = self.qualities
		if self.__qual_encoded:
			encoded_quality_str = "".join(map(lambda x: chr(x+33), self.qualities))
		result = "@%s\n%s\n+%s\n%s" % (self.header, self.sequence, header2, \
			encoded_quality_str)
		return result
		


	
	
	
		