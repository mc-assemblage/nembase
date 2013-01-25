from anduril.args import *
from ftplib import FTP
import csv


FTP_FILE_PATH = "/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/"


ftp = FTP("ftp-trace.ncbi.nih.gov")
ftp.login()
seqdir = FTP_FILE_PATH % (srarun[:3], srarun[:6], srarun)
write_log("NCBISRADownload: changing to ftp directory %s" % seqdir)
ftp.cwd(seqdir)
write_log("NCBISRADownload: retrieving sequence file %s.sra" % srarun)
ftp.retrbinary("RETR %s.sra" % srarun, open(srafile, 'wb').write)
ftp.quit()


