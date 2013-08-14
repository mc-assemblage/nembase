from anduril import constants
from ftplib import FTP
import anduril.main
import csv
import time


FTP_FILE_PATH = "/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/"


def sradownload(cf):
	"""Given an SRA accession, download the run file. There can be intermittent server 
		connection issues, so for this reason we implement a retry mechanism."""
	srarun = cf.get_parameter('srarun', 'string')
	tries = cf.get_parameter('retries', 'int') + 1
	while True:
		try:
			ftp = FTP('ftp-trace.ncbi.nih.gov')
			ftp.login()
			seqdir = FTP_FILE_PATH % (srarun[:3], srarun[:6], srarun)
			cf.write_log("NCBISRADownload: changing to ftp directory %s" % seqdir)
			ftp.cwd(seqdir)
			cf.write_log("NCBISRADownload: retrieving sequence file %s.sra" % srarun)
			ftp.retrbinary("RETR %s.sra" % srarun, open(\
				cf.get_output('srafile'), 'wb').write)
			ftp.quit()
			break
		except Exception, e:
			cf.write_error("NCBISRADownload error: %s" % str(e))
			tries = tries - 1
			if not tries > 0:
				return constants.GENERIC_ERROR
			else:
				cf.write_log("Retrying, attempts left %s" % tries)
				time.sleep(2)
	return constants.OK
	
	
anduril.main(sradownload)


