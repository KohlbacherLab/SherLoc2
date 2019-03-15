import re, os, sys, util

tmpfile_path=""
svm_path=""
firstN = 100
window_size = 20

def create_pattern(sequence, sa_start, sa_end, window_size, firstN):
	pattern = []
	for i in range (1,firstN+1):
		if i > len(sequence):
			break
		if i < (window_size-1)/2 + 1:
			start=1
		else:
			start = i - (window_size -1)/2
		if i + (window_size-1)/2 > len(sequence):
			end = len(sequence)
		else:
			end = i + (window_size-1)/2
		length = end - start +1
		if sa_start and sa_end and sa_end == "test" and  sa_start == "test":
			klasse = "0"
		elif sa_start and sa_end and i <= sa_end and i >= sa_start:
			klasse = "+1"
		else:
			klasse= "-1"
		input = []
		G_count= 0.0
		A_count= 0.0
		V_count= 0.0
		L_count= 0.0
		I_count= 0.0
		C_count= 0.0
		M_count= 0.0
		F_count= 0.0
		Y_count= 0.0
		W_count= 0.0
		P_count= 0.0
		S_count= 0.0
		T_count= 0.0
		N_count= 0.0
		Q_count= 0.0
		D_count= 0.0
		E_count= 0.0
		H_count= 0.0
		K_count= 0.0
		R_count= 0.0
		for k in range (start,end+1):
			aa = sequence[k-1]
			if aa == "G": G_count=G_count+1
			if aa == "A": A_count=A_count+1
			if aa == "V": V_count=V_count+1
			if aa == "L": L_count=L_count+1
			if aa == "I": I_count=I_count+1
			if aa == "C": C_count=C_count+1
			if aa == "M": M_count=M_count+1
			if aa == "F": F_count=F_count+1
			if aa == "Y": Y_count=Y_count+1
			if aa == "W": W_count=W_count+1
			if aa == "P": P_count=P_count+1
			if aa == "S": S_count=S_count+1
			if aa == "T": T_count=T_count+1
			if aa == "N": N_count=N_count+1
			if aa == "Q": Q_count=Q_count+1
			if aa == "D": D_count=D_count+1
			if aa == "E": E_count=E_count+1
			if aa == "H": H_count=H_count+1
			if aa == "K": K_count=K_count+1
			if aa == "R": R_count=R_count+1


		single_pattern=[]
		line = klasse
		G_count=float(G_count)/length
		line = line + " 1:"+str(G_count)
		A_count=float(A_count)/length
		line = line + " 2:"+str(A_count)
		V_count=float(V_count)/length
		line = line + " 3:"+str(V_count)
		L_count=float(L_count)/length
		line = line + " 4:"+str(L_count)
		I_count=float(I_count)/length
		line = line + " 5:"+str(I_count)
		C_count=float(C_count)/length
		line = line + " 6:"+str(C_count)
		M_count=float(M_count)/length
		line = line + " 7:"+str(M_count)
		F_count=float(F_count)/length
		line = line + " 8:"+str(F_count)
		Y_count=float(Y_count)/length
		line = line + " 9:"+str(Y_count)
		W_count=float(W_count)/length
		line = line + " 10:"+str(W_count)
		P_count=float(P_count)/length
		line = line + " 11:"+str(P_count)
		S_count=float(S_count)/length
		line = line + " 12:"+str(S_count)
		T_count=float(T_count)/length
		line = line + " 13:"+str(T_count)
		N_count=float(N_count)/length
		line = line + " 14:"+str(N_count)
		Q_count=float(Q_count)/length
		line = line + " 15:"+str(Q_count)
		D_count=float(D_count)/length
		line = line + " 16:"+str(D_count)
		E_count=float(E_count)/length
		line = line + " 17:"+str(E_count)
		H_count=float(H_count)/length
		line = line + " 18:"+str(H_count)
		K_count=float(K_count)/length
		line = line + " 19:"+str(K_count)
		R_count=float(R_count)/length
		line = line + " 20:"+str(R_count)+"\n"
		pattern.append(line)
	return pattern

def create_svm2_input(file_path,input_file,proteins,klasse,firstN,window_size,svm):
	file = open("%stest_svmsa_svm1.dat" % file_path, 'w')
	for i in range (0,len(proteins)):
		pattern = create_pattern(proteins[i]['sequence'],"test","test",window_size,firstN)
		for p in pattern:
			file.write(p)
	file.close()
	global svm_path
	os.system(svm_path+"/svm-predict -b 1 %stest_svmsa_svm1.dat %s %soutput_svmsa.dat > %sweg" % (file_path,svm,file_path,file_path))
	file_output = open("%soutput_svmsa.dat" % file_path, 'r')
	line=file_output.readline()
	for j in range (0,len(proteins)):
		input_file.write(klasse)
		n = 0
		pattern1 = "^-1\s|\s.+$"
		pattern2 ="^1\s.+\s"
		for i in range (1,firstN+1):
			n=n+1
			if i <=len(proteins[j]['sequence']):
				line = file_output.readline()
				line = re.sub("\n","",line)
				line = re.sub(" $","",line)
				if not line: val=0
				elif line[0] == "1":
					val=re.sub(pattern2,"",line)
					val=float(val)
				else:
					val=re.sub(pattern1,"",line)
					val=-1.0*float(val)
			else: val=0
			val=float(val)
			input_file.write(" "+str(n+1)+":"+str(val))

		input_file.write("\n")
	file_output.close()
	os.remove("%sweg" % file_path)
	os.remove("%stest_svmsa_svm1.dat" % file_path)
	os.remove("%soutput_svmsa.dat" % file_path)


def predict(origin,data,svm_model_path,libsvm_path,model=12345,id=1):
	global svm_path
	svm_path=libsvm_path
	file_path = tmpfile_path+"/"+str(id)
	model = str(model)

	svm1_sa = svm_model_path+"/svm_sa_%s_level1_benchmark80/%s.model" %(origin,model)
	svm2_sa = svm_model_path+"/svm_sa_%s_level2_benchmark80/%s.model" %(origin,model)

	result=[]
	proteins = util.parse_fasta_file(data)
	input_file = open("%stest_svmsa_svm2.dat" % file_path, 'w')
	create_svm2_input(file_path,input_file,proteins,"0",firstN,window_size,svm1_sa)
	input_file.close()

	os.system(svm_path+"/svm-predict -b 1 %stest_svmsa_svm2.dat %s %soutput_svm2_sa.dat > %sweg" % (file_path,svm2_sa,file_path,file_path))
	file_output_sa = open("%soutput_svm2_sa.dat" % file_path, 'r')
	line = file_output_sa.readline()
	pattern = "^1\s|^-1\s|\s.+$"
	pattern1 = "^1\s|\s.+$"
	pattern2 ="^-1\s.+\s"
	for i in range (0,len(proteins)):
		line = file_output_sa.readline()
		line = re.sub("\n","",line)
		line = re.sub(" $","",line)
		if not line: score_sa=0
		elif line[0] == "1":
			score_sa=re.sub(pattern1,"",line)
			score_sa=float(score_sa)
		else:
			score_sa=re.sub(pattern2,"",line)
			score_sa=-1.0*float(score_sa)
		score_sa=float(score_sa)

		result.append({'id':proteins[i]['id'],'score_sa':score_sa})
	file_output_sa.close()
	os.remove("%sweg" % file_path)
	os.remove("%stest_svmsa_svm2.dat" % file_path)
	os.remove("%soutput_svm2_sa.dat" % file_path)
	return result

def plant_predict(data,svm_model_path,libsvm_path,model=12345,id=1):
	return predict("plant",data,svm_model_path,libsvm_path,model,id)

def noplant_predict(data,svm_model_path,libsvm_path,model=12345,id=1):
	return predict("noplant",data,svm_model_path,libsvm_path,model,id)
