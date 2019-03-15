import os, sys, re

class Error(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def search_program(program, warning):
	path =""
	print "searching for %s ... " %(program)
	path = run_shell_command("which " + program)
	if (path != ""):
		print "... found: %s" %(path)
		print
		return re.sub(program+"$","",path)
	elif warning == 1:
		print "Warning: %s not found!" %(program)
		print "It is recommended but not required to install %s and to include its path into your $PATH variable!" %(program)
		return path
	else:
		msg = "Error: %s not found!" %(program)
		msg = msg + " Include the path to %s into your $PATH variable and restart python configure.py!" %(program)
		raise Error(msg)

def run_shell_command(cmd):
	stdout_handle = os.popen(cmd, "r")
	return re.sub("\n","",stdout_handle.read())

def set_path_in_src_files(type,path,src_path):
	cmd= "sed -i 's/%s\s*=\s*\"[^\"]*\"/%s=\"" %(type,type)
	cmd = cmd + re.sub("/","\\/",path) + "\"/g' " + src_path + "*.py"
	run_shell_command(cmd)

#main program
print ""
print "Start SherLoc2 configuration:"
print ""

sherloc2_path = "/SherLoc2/"
tmp_file_path = "/tmp/"
src_path = sherloc2_path + "/src/"
svm_data_path = sherloc2_path + "/data/svm_models/SherLoc2/"
genome_path =  sherloc2_path + "/data/NCBI/"

python_path = search_program("python",0)
svm_predict_path = search_program("svm-predict",0)
blast_path = search_program("blastp",0)
formatdb_path = search_program("makeblastdb",0)
inter_pro_scan_path = search_program("interproscan.sh",1)

print "\nset all static paths in source files ..."
#all is fine here
set_path_in_src_files("sherloc2_path",sherloc2_path+"/",src_path)
set_path_in_src_files("src_path",src_path,src_path)
set_path_in_src_files("tmpfile_path",tmp_file_path,src_path)
set_path_in_src_files("svm_data_path",svm_data_path,src_path)
set_path_in_src_files("genome_path",genome_path,src_path)
set_path_in_src_files("libsvm_path",svm_predict_path,src_path)
set_path_in_src_files("blast_path",blast_path,src_path)
set_path_in_src_files("formatdb_path",formatdb_path,src_path)
set_path_in_src_files("inter_pro_scan_path",inter_pro_scan_path,src_path)
set_path_in_src_files("python_path",python_path,src_path)

#print "... create script run_sherloc2_with_iprscan"
#file = open("run_sherloc2_with_iprscan","w")
#file.write("%siprscan -cli -i $1 -o interpro.out -format raw -goterms -iprlookup\n" %(inter_pro_scan_path))
#file.write("python %ssherloc2_prediction.py -fasta=$1 -origin=$2 -result=$3 -go=interpro.out" %(src_path))
#file.close()
#os.system("chmod 755 run_sherloc2_with_iprscan")

print "... completed"

print "\nset all required rights to write temporary files ..."

os.system("chmod a+w data/NCBI/genomes/Archaea")
os.system("chmod a+w data/NCBI/genomes/Eukaryota")
os.system("chmod a+w data/NCBI/genomes/Bacteria/all")

print "... completed"
print "SherLoc2 is ready to use!"
