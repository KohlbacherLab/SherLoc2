import re,sys,os,string, time, probability_estimate

class Timeout(Exception):
	pass

class Error(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def parse_fasta_file(data):
	try:
		file = data
		tmp = file.tell()
	except AttributeError:
		file = open(data, 'r')
	id=""
	sequence=""
	proteins=[]
	line = file.readline()
	if line[0] != ">": raise Error("wrong format in fasta file %s!" % data)
	id = re.sub("^>","",line)
	id = re.findall("^[\S]+", id)
	if len(id) == 0:
		id = "Seq 1"
	else:
		id = id[0]
	i=0
	proteins.append({'id':id,'sequence':""})
	while 1:
		line = file.readline()
		if i==0 and not line and not sequence: raise Error("wrong format in fasta file %s!" % data)
		if i>0 and not sequence and not line: raise Error("wrong format in fasta file %s!" % data)
		if not line: break
		if line[0] == ">":
			if sequence == "": raise Error("wrong format in fasta file %s!" % data)
			proteins[i]['sequence']=sequence
			sequence = ""
			i=i+1
			id = re.sub("^>","",line)
			id = re.findall("^[\S]+", id)
			if len(id) == 0:
				id = "Seq %s" %(i+1)
			else:
				id = id[0]
			proteins.append({'id':id,'sequence':""})
		else:
			if (re.findall("[A-Za-z]+",line)):
				sequence += re.findall("[A-Za-z]+",line)[0]
	proteins[i]['sequence']=sequence
	return proteins

def validate_not_empty(paths):
	for path in paths:
		if path == "":
			raise Error("Configuration Error: A path is not set. Run configure script!")

def predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins):
	nr_loc = 0
	version = string.lower(table)
	svm = []
	ergebnis=[]
	result=[]

	cmd0=libsvm_path+"/svm-predict -b 1 "
	file_path = tmpfile_path+"/"+str(id)

	if re.findall("Benchmark80",table):
		nr_loc=9
		if origin == "plant":
			nr_loc=10
	if re.findall("TargetP",table):
		nr_loc=3
		if origin == "plant":
			nr_loc=4
	if re.findall("BACELLO",table):
		nr_loc=4
		if origin == "plant":
			nr_loc=5

	if re.findall("BACELLO",table):
		svm.append(path+"%s_nuc_vs_cyt_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_mit_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_nuc_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_ext_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_mit_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_cyt_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_ext_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_mit_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_ext_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_chl_vs_ext_%s/%s.model" %(origin,version,model))

	if re.findall("Benchmark80",table):
		svm.append(path+"%s_nuc_vs_cyt_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_mit_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_nuc_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_ext_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_pm_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_per_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_nuc_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_nuc_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_nuc_vs_vac_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_mit_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_cyt_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_ext_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_pm_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_per_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_cyt_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_cyt_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_cyt_vs_vac_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_mit_vs_chl_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_ext_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_pm_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_per_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_mit_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_mit_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_mit_vs_vac_%s/%s.model" %(origin,version,model))
		if origin == "plant":
			svm.append(path+"%s_chl_vs_ext_%s/%s.model" %(origin,version,model))
			svm.append(path+"%s_chl_vs_pm_%s/%s.model" %(origin,version,model))
			svm.append(path+"%s_chl_vs_per_%s/%s.model" %(origin,version,model))
			svm.append(path+"%s_chl_vs_er_%s/%s.model" %(origin,version,model))
			svm.append(path+"%s_chl_vs_gol_%s/%s.model" %(origin,version,model))
			svm.append(path+"%s_chl_vs_vac_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_ext_vs_pm_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_ext_vs_per_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_ext_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_ext_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_ext_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_ext_vs_vac_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_pm_vs_per_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_pm_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_pm_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_pm_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_pm_vs_vac_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_per_vs_er_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_per_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_per_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_per_vs_vac_%s/%s.model" %(origin,version,model))
		svm.append(path+"%s_er_vs_gol_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_er_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_er_vs_vac_%s/%s.model" %(origin,version,model))
		if origin == "animal":
			svm.append(path+"%s_gol_vs_lys_%s/%s.model" %(origin,version,model))
		else:
			svm.append(path+"%s_gol_vs_vac_%s/%s.model" %(origin,version,model))

	if re.findall("TargetP",table):
		if origin == "plant":
			svm.append(path+"plant_mit_vs_chl_%s/%s.model" %(version,model))
			svm.append(path+"plant_mit_vs_sp_%s/%s.model" %(version,model))
			svm.append(path+"plant_mit_vs_oth_%s/%s.model" %(version,model))
			svm.append(path+"plant_chl_vs_sp_%s/%s.model" %(version,model))
			svm.append(path+"plant_chl_vs_oth_%s/%s.model" %(version,model))
			svm.append(path+"plant_sp_vs_oth_%s/%s.model" %(version,model))
		else:
			svm.append(path+"non-plant_mit_vs_sp_%s/%s.model" %(version,model))
			svm.append(path+"non-plant_mit_vs_oth_%s/%s.model" %(version,model))
			svm.append(path+"non-plant_sp_vs_oth_%s/%s.model" %(version,model))

	pattern = "^1\s|^0\s|\s.+$"
	for i in range(0,len(svm)):
		result.append([])
		cmd=cmd0 + "%stest_svm.dat %s %soutputsvmbm > %sweg" %(file_path,svm[i],file_path,file_path)
		os.system(cmd)
		file=open("%soutputsvmbm" %(file_path))
		line=file.readline()
		while (1):
			line=file.readline()
			if not line: break
			line = re.sub("\n","",line)
			line = re.sub(" $","",line)
			score=re.sub(pattern,"",line)
			result[i].append(score)
		file.close()

	estimated_probs=[]
	for i in range(len(result[0])):
		probs = []
		for j in range(len(result)):
			probs.append(result[j][i])
		estimated_probs.append(probability_estimate.estimate(nr_loc,probs))

	k=0
	for i in range (0,len(proteins)):
		if proteins[i]['id'] in no_fv_proteins:
			if re.findall("Benchmark80",table):
				if origin == "animal":
					ergebnis.append({'id':proteins[i]['id'],'score_nuc':0.11,'score_cyt':0.11,'score_mit':0.11,'score_per':0.11,'score_lys':0.11,'score_er':0.11,'score_gol':0.11,'score_ext':0.11,'score_pm':0.11})
				elif origin == "fungi":
					ergebnis.append({'id':proteins[i]['id'],'score_nuc':0.11,'score_cyt':0.11,'score_mit':0.11,'score_per':0.11,'score_vac':0.11,'score_er':0.11,'score_gol':0.11,'score_ext':0.11,'score_pm':0.11})
				else:
					ergebnis.append({'id':proteins[i]['id'],'score_nuc':0.1,'score_cyt':0.1,'score_mit':0.1,'score_chl':0.1,'score_per':0.1,'score_vac':0.1,'score_er':0.1,'score_gol':0.1,'score_ext':0.1,'score_pm':0.1})
			if re.findall("BACELLO",table):
				if origin == "plant":
					ergebnis.append({'id':proteins[i]['id'],'score_nuc':0.2,'score_cyt':0.2,'score_mit':0.2,'score_chl':0.2,'score_ext':0.2})
				else:
					ergebnis.append({'id':proteins[i]['id'],'score_nuc':0.25,'score_cyt':0.25,'score_mit':0.25,'score_ext':0.25})
			if re.findall("TargetP",table):
				if origin == "plant":
					ergebnis.append({'id':proteins[i]['id'],'score_mit':0.25,'score_chl':0.25,'score_sp':0.25,'score_oth':0.25})
				else:
					ergebnis.append({'id':proteins[i]['id'],'score_mit':0.33,'score_sp':0.33,'score_oth':0.33})
			continue

		if re.findall("Benchmark80",table):
			if origin == "animal":
				score_nuc = float(estimated_probs[k][0])
				score_cyt = float(estimated_probs[k][1])
				score_mit = float(estimated_probs[k][2])
				score_ext = float(estimated_probs[k][3])
				score_pm = float(estimated_probs[k][4])
				score_per = float(estimated_probs[k][5])
				score_er = float(estimated_probs[k][6])
				score_gol = float(estimated_probs[k][7])
				score_lys = float(estimated_probs[k][8])
				score_nuc_vs_cyt = float(result[0][k])
				ergebnis.append({'id':proteins[i]['id'],'score_nuc':score_nuc,'score_nuc_vs_cyt':score_nuc_vs_cyt,'score_cyt':score_cyt,'score_mit':score_mit,'score_per':score_per,'score_lys':score_lys,'score_er':score_er,'score_gol':score_gol,'score_ext':score_ext,'score_pm':score_pm})
			elif origin == "fungi":
				score_nuc = float(estimated_probs[k][0])
				score_cyt = float(estimated_probs[k][1])
				score_mit = float(estimated_probs[k][2])
				score_ext = float(estimated_probs[k][3])
				score_pm = float(estimated_probs[k][4])
				score_per = float(estimated_probs[k][5])
				score_er = float(estimated_probs[k][6])
				score_gol = float(estimated_probs[k][7])
				score_vac = float(estimated_probs[k][8])
				score_nuc_vs_cyt = float(result[0][k])
				ergebnis.append({'id':proteins[i]['id'],'score_nuc':score_nuc,'score_nuc_vs_cyt':score_nuc_vs_cyt,'score_cyt':score_cyt,'score_mit':score_mit,'score_per':score_per,'score_vac':score_vac,'score_er':score_er,'score_gol':score_gol,'score_ext':score_ext,'score_pm':score_pm})
			else:
				score_nuc = float(estimated_probs[k][0])
				score_cyt = float(estimated_probs[k][1])
				score_mit = float(estimated_probs[k][2])
				score_chl = float(estimated_probs[k][3])
				score_ext = float(estimated_probs[k][4])
				score_pm = float(estimated_probs[k][5])
				score_per = float(estimated_probs[k][6])
				score_er = float(estimated_probs[k][7])
				score_gol = float(estimated_probs[k][8])
				score_vac = float(estimated_probs[k][9])
				score_nuc_vs_cyt = float(result[0][k])
				ergebnis.append({'id':proteins[i]['id'],'score_nuc':score_nuc,'score_nuc_vs_cyt':score_nuc_vs_cyt,'score_cyt':score_cyt,'score_mit':score_mit,'score_chl':score_chl,'score_per':score_per,'score_vac':score_vac,'score_er':score_er,'score_gol':score_gol,'score_ext':score_ext,'score_pm':score_pm})
		if re.findall("TargetP",table):
			if origin == "plant":
				score_mit = float(estimated_probs[k][0])
				score_chl = float(estimated_probs[k][1])
				score_sp = float(estimated_probs[k][2])
				score_oth = float(estimated_probs[k][3])
				ergebnis.append({'id':proteins[i]['id'],'score_mit':score_mit,'score_chl':score_chl,'score_sp':score_sp,'score_oth':score_oth})
			else:
				score_mit = float(estimated_probs[k][0])
				score_sp = float(estimated_probs[k][1])
				score_oth = float(estimated_probs[k][2])
				ergebnis.append({'id':proteins[i]['id'],'score_mit':score_mit,'score_sp':score_sp,'score_oth':score_oth})

		if re.findall("BACELLO",table):
			if origin == "plant":
				score_nuc = float(estimated_probs[k][0])
				score_cyt = float(estimated_probs[k][1])
				score_mit = float(estimated_probs[k][2])
				score_chl = float(estimated_probs[k][3])
				score_ext = float(estimated_probs[k][4])
				score_nuc_vs_cyt = float(result[0][k])
				ergebnis.append({'id':proteins[i]['id'],'score_mit':score_mit,'score_chl':score_chl,'score_cyt':score_cyt,'score_ext':score_ext,'score_nuc':score_nuc,'score_nuc_vs_cyt':score_nuc_vs_cyt})
			else:
				score_nuc = float(estimated_probs[k][0])
				score_cyt = float(estimated_probs[k][1])
				score_mit = float(estimated_probs[k][2])
				score_ext = float(estimated_probs[k][3])
				score_nuc_vs_cyt = float(result[0][k])
				ergebnis.append({'id':proteins[i]['id'],'score_mit':score_mit,'score_cyt':score_cyt,'score_ext':score_ext,'score_nuc':score_nuc,'score_nuc_vs_cyt':score_nuc_vs_cyt})
		k=k+1

	os.remove("%soutputsvmbm" % file_path)
	os.remove("%sweg" % file_path)
	os.remove("%stest_svm.dat" % file_path)

	return ergebnis
