from create_snapshot import NCBITranscriptomeRunData
from optparse import OptionParser
import cPickle as pickle
import csv
import sys
import xlwt


usage = "usage: %prog [options] <snapshot.pkl> <exp.completed> <output.xls>"
parser = OptionParser(usage=usage)


def isRunComplete(runData, platform, exp_completed):
	"""Return true if run is complete."""
	parts = platform.split(',')
	completed = True
	for part in parts:
		if part == 'Genome':
			continue
		elif part == 'ESTs':
			continue
		elif part == 'Illumina':
			for exp_accession in runData.expsIllumina.keys():
				if not exp_accession in exp_completed:
					completed = False
					break
		else:
			continue
			#for exp_accession in runData.exps454.keys():
			#	if not exp_accession in exp_completed:
			#		completed = False
			#		break
	return completed


def getRowStyle(runData, platform, exp_completed):
	"""Return the appropriate style for row."""
	style = xlwt.XFStyle()
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	if platform == "No Data":
		pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
		style.pattern = pattern
	elif isRunComplete(runData, platform, exp_completed):
		pattern.pattern_fore_colour = xlwt.Style.colour_map['green']
		style.pattern = pattern
	return style


def getOrganismListByPlatforms(platformstr, snapshot):
	"""Return a list of organisms that have data in each of the platforms in 
		platformstr."""
	platformlist = platformstr.split(',')
	if platformstr == "No Data":
		platformlist = []
	platformlist.sort()
	orglist = []
	for org in snapshot.keys():
		if platformstr == 'Genome' and \
			snapshot[org].genomeData:
			orglist.append(org)
			continue
		elif snapshot[org].genomeData:
			continue
		tmp_platforms = []
		if len(snapshot[org].accessionsEST) > 0:
			tmp_platforms.append('ESTs')
		if len(snapshot[org].expsIllumina) > 0:
			tmp_platforms.append('Illumina')
		if len(snapshot[org].exps454) > 0:
			tmp_platforms.append('454')
		tmp_platforms.sort()
		if tmp_platforms == platformlist:
			orglist.append(org)
	return orglist
	
	
def write_row(write, nrow, cols, style=None):
	"""Write a complete row to an EXCEL sheet."""
	for i in range(0, len(cols)):
		if style:
			write(nrow, i, cols[i], style)
		else:
			write(nrow, i, cols[i])


def createNembaseStatusReport(snapshot_pkl, exp_completed, xlsout):
	"""Create an EXCEL workbook containing the status of the NEMBASE workflow."""
	headercols = ['Organism', 'EST Count', '454 Exp Count', 'Illumina Exp Count', ' ']
	statuscols = ['Genome', 'ESTs', '454', 'Illumina', 'ESTs,454', 'ESTs,Illumina', \
		'Illumina,454', 'ESTs,454,Illumina', 'No Data']
	snapshot = pickle.load(open(snapshot_pkl, 'rb'))
	book = xlwt.Workbook()
	sheet = book.add_sheet('Nembase Status')
	write_row(sheet.write, 0, headercols + statuscols)
	row_index = 1
	for col in statuscols:
		filteredList = getOrganismListByPlatforms(col, snapshot)
		filteredList.sort()
		for org in filteredList:
			row = [' '] * (len(headercols)+len(statuscols))
			row[0] = org
			if len(snapshot[org].accessionsEST) > 0:
				row[1] = len(snapshot[org].accessionsEST)
			if len(snapshot[org].exps454) > 0:
				row[2] = len(snapshot[org].exps454)
			if len(snapshot[org].expsIllumina) > 0:
				row[3] = len(snapshot[org].expsIllumina)
			row[statuscols.index(col)+len(headercols)] = 'X'
			write_row(sheet.write, row_index, row, \
				getRowStyle(snapshot[org], col, exp_completed))
			row_index += 1
	book.save(xlsout)


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 3:
		parser.print_help()
		sys.exit(2)
	reader = csv.reader(open(args[1], 'rb'), delimiter='\t')
	exp_completed = []
	for row in reader:
		if not len(row) > 0:
			continue
		exp_completed.append(row[0])
	createNembaseStatusReport(args[0], exp_completed, args[2])
	
	
	