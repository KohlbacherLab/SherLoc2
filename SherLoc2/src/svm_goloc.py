import re,sys,os,string, time, util

svm_path=""
tmpfile_path=""

all_animal_go_terms = []
all_fungi_go_terms = []
all_plant_go_terms = []

use_go_files = 0
protein_go_fvector = {}

def process_go_files(origin,go_file_names):
	if len(go_file_names) > 0:
		use_go_files = 1
	protein_go_terms = {}
	for go_file_name in go_file_names:
		file = open(go_file_name,"r")
		line = ""
		while 1:
			line = file.readline()
			if not line: break
			line =re.sub("\n","",line)
			tokens = re.findall("^\S+\s",line)
			if len(tokens)>0:
				protein_id = re.sub("\s$","",tokens[0])
				tokens = re.findall("GO:\d+",line)
				for token in tokens:
					go_term = re.sub("GO:","",token)
					go_term = re.sub("^0*","",go_term)
					go_term = int(go_term)
					if origin=="animal" and go_term not in all_animal_go_terms:
						continue
					if origin=="fungi" and go_term not in all_fungi_go_terms:
						continue
					if origin=="plant" and go_term not in all_plant_go_terms:
						continue
					if protein_id not in protein_go_terms:
						protein_go_terms[protein_id]=[]
					if go_term not in protein_go_terms[protein_id]:
						protein_go_terms[protein_id].append(go_term)
		file.close()
	for protein_id in protein_go_terms.keys():
		found_go_terms = protein_go_terms[protein_id]
		found_go_terms.sort()
		fv = ""
		for go_term in found_go_terms:
			if fv == "":
				fv = fv + str(go_term) + ":1.0"
			else:
				fv = fv + " " + str(go_term) + ":1.0"
		protein_go_fvector[protein_id] = fv

def create_feature_vector(inter_pro_scan_path,origin,sequence,id,protein_id):
	file_path = tmpfile_path+"/"+str(id)
	fv = ""
	if use_go_files == 1:
		if protein_id in protein_go_fvector.keys():
			fv = protein_go_fvector[protein_id]
	else:
		file = open("%stest.seq" %(file_path),"w")
		file.write(">query_seq\n"+sequence+"\n")
		file.close()
		cmd = "nice -n 19 " + inter_pro_scan_path + "/iprscan -cli -i %stest.seq -o %stest.out -format raw -goterms -iprlookup" %(file_path,file_path)
		os.system(cmd)
		file=open("%stest.out" %(file_path),"r")
		line=""
		found_go_terms=[]
		while 1:
			line = file.readline()
			if not line: break
			line =re.sub("\n","",line)
			tokens = re.findall("GO:\d+",line)
			for token in tokens:
				go_term = re.sub("GO:","",token)
				go_term = re.sub("^0*","",go_term)
				go_term = int(go_term)
				if origin=="animal" and go_term not in all_animal_go_terms:
					continue
				if origin=="fungi" and go_term not in all_fungi_go_terms:
					continue
				if origin=="plant" and go_term not in all_plant_go_terms:
					continue
				if go_term not in found_go_terms:
					found_go_terms.append(go_term)
		file.close()

		found_go_terms.sort()
		for go_term in found_go_terms:
			if fv == "":
				fv = fv + str(go_term) + ":1.0"
			else:
				fv = fv + " " + str(go_term) + ":1.0"
		os.remove("%stest.seq" % file_path)
		os.remove("%stest.out" % file_path)
	return fv

def predict(origin,table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id=1):
	model=str(model)
	if origin == "animal":
		global all_animal_go_terms
		all_animal_go_terms = []
	elif origin == "fungi":
		global all_fungi_go_terms
		all_fungi_go_terms = []
	else:
		global all_plant_go_terms
		all_plant_go_terms = []
	if re.findall("Benchmark80",table) or re.findall("BACELLO",table):
		fname = path+"/benchmark80_animal_go_terms.dat"
		if origin == "fungi":
			fname = path+"/benchmark80_fungi_go_terms.dat"
		if origin == "plant":
			fname = path+"/benchmark80_plant_go_terms.dat"
		if re.findall("BACELLO",table):
			fname = path+"/bacello_animal_go_terms.dat"
			if origin == "fungi":
				fname = path+"/bacello_fungi_go_terms.dat"
			if origin == "plant":
				fname = path+"/bacello_plant_go_terms.dat"
		file = open(fname,"r")
		line = ""
		while 1:
			line = file.readline()
			if not line: break
			line  = re.sub("\n","",line)
			go_term = int(line)
			if origin == "animal":
				all_animal_go_terms.append(go_term)
			elif origin == "fungi":
				all_fungi_go_terms.append(go_term)
			else:
				all_plant_go_terms.append(go_term)
		file.close()
	global protein_go_fvector
	protein_go_fvector = {}
	global use_go_files
	if use_inter_pro_scan == 0:
		use_go_files = 1
	if use_go_files == 1:
		process_go_files(origin, go_file_names)

	proteins = util.parse_fasta_file(data)

	file_path = tmpfile_path+"/"+str(id)
	input_file = open("%stest_svm.dat" % file_path, 'w')
	no_fv_proteins=[]
	for i in range (0,len(proteins)):
		fv = create_feature_vector(inter_pro_scan_path,origin,proteins[i]['sequence'],id,proteins[i]['id'])
		if fv != "":
			fv = "0 " + fv
			input_file.write(fv+"\n")
		else:
			no_fv_proteins.append(proteins[i]['id'])
			if use_go_files == 1 and len(go_file_names) > 0:
				print "warning: no GO terms found for protein with id: %s" %(proteins[i]['id'])
	input_file.close()

	return util.predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins)

def animal_predict(table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id=1):
	return predict("animal",table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id)

def fungi_predict(table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id=1):
	return predict("fungi",table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id)

def plant_predict(table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id=1):
	return predict("plant",table,path,data,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names, id)
