import re,sys,os,string,math,time,util

svm_path=""
tmpfile_path=""
genome_path=""
blast_path=""
formatdb_path=""

protein_self_bit_score_map = {}

def createSelfBitScores(filename):
	global protein_self_bit_score_map
	protein_self_bit_score_map = {}
	ifile=open(filename,'r')
	while 1:
		line=ifile.readline()
		if not line: break
		line=re.sub("\n","",line)
		line=re.sub("\s+","\t",line)
		tokens = line.split("\t")
		if len(tokens)==12 and tokens[0] == tokens[1]:
			if tokens[0] in protein_self_bit_score_map:
				continue
			protein_self_bit_score_map[tokens[0]]=float(tokens[11])
	ifile.close()


def createProfile(fastafile, blast_path, genome_path, sessionid=1):
	file_path = tmpfile_path+"/"+str(sessionid)
	query_path = "%squeryfilePhylo.txt" %(file_path)
	parse_path = "%sparsefilePhylo.txt" %(file_path)
	blast_out_path = "%sphylo_blastoutput/" %(file_path)
	line=""
	result=[]
	ergebnis=[]
	proteins = {}
	proteins2 = {}
	if os.path.exists(blast_out_path):
		cmd = "rm -r " + blast_out_path
		os.system(cmd)
	os.mkdir(blast_out_path)

	queryFile = file(query_path, 'w+')
	queryList = fastafile.readlines()
	queryFile.writelines(queryList)
	queryFile.close()

	genomeList = []
	lfile=open(genome_path+"/ordered_ncbi_taxIDs.dat",'r')
	while 1:
		line=lfile.readline()
		if not line: break
		line=re.sub("\n","",line) + ".faa"
		genomeList.append(line)
	lfile.close()
	lfile=open(genome_path+"/ordered_ncbi_taxIDs_archaea.dat",'r')
	while 1:
		line=lfile.readline()
		if not line: break
		line=re.sub("\n","",line) + ".faa"
		genomeList.append(line)
	lfile.close()
	lfile=open(genome_path+"/ordered_ncbi_taxIDs_eukaryota.dat",'r')
	while 1:
		line=lfile.readline()
		if not line: break
		line=re.sub("\n","",line) + ".faa"
		genomeList.append(line)
	lfile.close()
	for i in range(len(genomeList)):
		if i>24 and i <400:
			continue
		db_path = genome_path+"/genomes/Bacteria/all/" + genomeList[i]
		if i >=400 and i <433:
			db_path = genome_path+"/genomes/Archaea/" + genomeList[i]
		if i >=433:
			db_path = genome_path+"/genomes/Eukaryota/" + genomeList[i]
		blastoutput_path = blast_out_path + '/' + genomeList[i] + '.txt'
		#if os.path.exists(db_path + ".pin") == False:
		#	os.system(formatdb_path + "/formatdb" + " -i " + db_path)
		#cmd = "nice -n 19 " +blast_path + "/blastall -p blastp  -d " + db_path +  " -i " + query_path + "   -m9  -o " + blastoutput_path

		blastoutput_path = blast_out_path + '/' + genomeList[i] + '.txt'
		if os.path.exists(db_path + ".pin") == False:
			cmd = "nice -n 19 " + blast_path + "/makeblastdb -in " + db_path + " -dbtype prot"
			os.system(cmd)

		cmd = "nice -n 19 " + blast_path + "/blastp  -db " + db_path +  " -query " + query_path + " -outfmt 7 -out " + blastoutput_path
		os.system(cmd)

	for id in protein_self_bit_score_map.keys():
		proteins[id]=[]
		proteins2[id]=[]
		for i in range(len(genomeList)):
			proteins[id].append(0.0)
			proteins2[id].append(0.0)

	for i in range(len(genomeList)):
		if i>24 and i <400:
			continue

		blastFile = file(blast_out_path + '/' + genomeList[i] + '.txt' ,'r')
		blastLines = blastFile.readlines()

		id = blastLines[1].split(" ")[2].strip()

		phylovalue = {}
		phylovalue[0.1] = 0.0
		phylovalue[0.01] = 0.0
		phylovalue[0.001] = 0.0
		phylovalue[0.0001] = 0.0
		phylovalue[0.00001] = 0.0
		phylovalue[0.000001] = 0.0
		phylovalue[0.0000001] = 0.0
		phylovalue[0.00000001] = 0.0
		phylovalue[0.000000001] = 0.0
		phylovalue[0.0000000001] = 0.0

		# berpruefung, ob es ueberhaupt ein blast-ergebnis gibt
		bit_score = 0.0

		if len(blastLines) >= 6:
			hit_line = blastLines[5].split("\t")
			evalue = hit_line[10]
			bit_score_raw = hit_line[11]

			if id in protein_self_bit_score_map:
				bit_score = float(bit_score_raw) / protein_self_bit_score_map[id]
			if evalue != "0.0":
				for cutoff in phylovalue.keys():
					if float(evalue) >= cutoff:
						phylovalue[cutoff] = 1.0
					else:
						phylovalue[cutoff] = -1.0 /(math.log10(float(evalue)))
		else:
			evalue = 1
			for cutoff in phylovalue.keys():
				phylovalue[cutoff] = 1.0

		proteins2[id][i]=bit_score

		"""
		for k in range(len(blastLines)):
			if blastLines[k].find("# Query") != -1:
				id = blastLines[k][9:]
				id = re.sub("\n","",id)
				tokens = id.split(" ")
				id = tokens[0]
				phylovalue = {}
				phylovalue[0.1] = 0.0
				phylovalue[0.01] = 0.0
				phylovalue[0.001] = 0.0
				phylovalue[0.0001] = 0.0
				phylovalue[0.00001] = 0.0
				phylovalue[0.000001] = 0.0
				phylovalue[0.0000001] = 0.0
				phylovalue[0.00000001] = 0.0
				phylovalue[0.000000001] = 0.0
				phylovalue[0.0000000001] = 0.0

				# berpruefung, ob es ueberhaupt ein blast-ergebnis gibt
				bit_score = 0.0
				if (k+4 <= len(blastLines)) and (blastLines[k+3].find("BLASTP") == -1):
					evalLine = blastLines[k+3].split("\t")
					evalue = evalLine[10]
					if id in protein_self_bit_score_map:
						bit_score = float(evalLine[11]) / protein_self_bit_score_map[id]
					if evalue != "0.0":
						for cutoff in phylovalue.keys():
							if float(evalue) >= cutoff:
								phylovalue[cutoff] = 1.0
							else:
								phylovalue[cutoff] = -1.0 /(math.log10(float(evalue)))

				#gibt es kein blast-ergebnis wird der evalue und phylovalue auf 1 gesetzt
				else:
					evalue = 1
					for cutoff in phylovalue.keys():
						phylovalue[cutoff] = 1.0

				proteins2[id][i]=bit_score
		"""

		blastFile.close()


	res = []
	for ac in proteins2.keys():
		evalues = proteins2[ac]
		featurevector = ""
		for i in range(0,len(evalues)):
			if i>24 and i <400:
				continue
			if i==0:
				featurevector="%s:%s" %(i+1,evalues[i])
			else:
				featurevector=featurevector + " %s:%s" %(i+1,evalues[i])
		ac = ac.split(" ")[0]
		res.append(featurevector)

	if os.path.exists(query_path):
		os.remove(query_path)
	if os.path.exists(parse_path):
		os.remove(parse_path)
	if os.path.exists(blast_out_path):
		cmd = "rm -r " + blast_out_path
		os.system(cmd)
	return res

def create_feature_vector(protein_id,sequence,blast_path,genome_path,id=1):
	file_path = tmpfile_path+"/"+str(id)
	fv = ""
	file = open("%stest.seq" %(file_path),"w")
	file.write(">"+protein_id+"\n"+sequence+"\n")
	file.close()
	#cmd = "nice -n 19 "+formatdb_path+"/formatdb -i %stest.seq" %(file_path)
	cmd = "nice -n 19 "+blast_path+"/makeblastdb -in %stest.seq -dbtype prot" %(file_path)
	os.system(cmd)
	#cmd = "nice -n 19 "+blast_path+"/blastall -p blastp  -d %stest.seq -i %stest.seq -m9 -o %stest_blast.txt" %(file_path,file_path,file_path)
	cmd = "nice -n 19 "+blast_path+"/blastp  -db %stest.seq -query %stest.seq -outfmt 7 -out %stest_blast.txt" %(file_path,file_path,file_path)
	os.system(cmd)
	fastafile = open("%stest.seq" %(file_path), 'r')
	inputfile = os.tmpfile()
	line=fastafile.readlines()
	inputfile.writelines(line)
	inputfile.seek(0)
	createSelfBitScores("%stest_blast.txt" %(file_path))
	fvs = createProfile(inputfile,blast_path,genome_path,id)
	fv=""
	if len(fvs) > 0:
		fv=fvs[0]
	fastafile.close()
	inputfile.close()

	if os.path.exists("%stest.seq" % file_path):
		os.remove("%stest.seq" % file_path)
	if os.path.exists("%stest.seq.phr" % file_path):
		os.remove("%stest.seq.phr" % file_path)
	if os.path.exists("%stest.seq.pin" % file_path):
		os.remove("%stest.seq.pin" % file_path)
	if os.path.exists("%stest.seq.psq" % file_path):
		os.remove("%stest.seq.psq" % file_path)
	if os.path.exists("%stest_blast.txt" % file_path):
		os.remove("%stest_blast.txt" % file_path)
	if os.path.exists("%stest.out" % file_path):
		os.remove("%stest.out" % file_path)
	return fv

def predict(origin,table,path,data,model,libsvm_path,blast_path,genome_path, id=1):
    model=str(model)

    proteins = util.parse_fasta_file(data)

    file_path = tmpfile_path+"/"+str(id)
    input_file = open("%stest_svm.dat" % file_path, 'w')
    no_fv_proteins=[]
    for i in range (0,len(proteins)):
        fv = create_feature_vector(proteins[i]['id'],proteins[i]['sequence'],blast_path,genome_path,id)
        if fv != "":
            fv = "0 " + fv
            input_file.write(fv+"\n")
        else:
            no_fv_proteins.append(proteins[i]['id'])
    input_file.close()

    return util.predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins)

def animal_predict(table,path,data,model,libsvm_path,blast_path,genome_path, id=1):
	return predict("animal",table,path,data,model,libsvm_path,blast_path,genome_path, id)

def fungi_predict(table,path,data,model,libsvm_path,blast_path,genome_path, id=1):
	return predict("fungi",table,path,data,model,libsvm_path,blast_path,genome_path, id)

def plant_predict(table,path,data,model,libsvm_path,blast_path,genome_path, id=1):
	return predict("plant",table,path,data,model,libsvm_path,blast_path,genome_path, id)
