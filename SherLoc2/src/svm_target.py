import re, os, sys, time, util

svm_path=""
tmpfile_path=""

firstN_plant = 100
firstN_noplant = 60

window_size_plant_ctp_vs_mtp = 20
window_size_plant_ctp = 55
window_size_plant_mtp = 34
window_size_plant_sp = 24
window_size_noplant_mtp = 34
window_size_noplant_sp = 23

window_size_ctp=55
window_size_sp=23
window_size_mtp=34
firstN_mtp=60
firstN_ctp=100
firstN_sp=60

def create_pattern(sequence, cleavage_site, window_size, firstN):
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
		if cleavage_site and cleavage_site == "test":
			klasse = "0"
		elif cleavage_site and i <= cleavage_site:
			klasse = "+1"
		else:
			klasse= "-1"
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

def create_pattern2(sequence,klasse):
	if len(sequence) >=15:
		sequence = re.findall("^.{15}",sequence)[0]
	pattern = []
	for i in range (1,2):
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
		for k in range (0,len(sequence)):
			aa = sequence[k]
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

		length=len(sequence)
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


def create_svm2_input(origin,file_path,input_file,mtp_ctp_file,proteins,klasse,firstN_sp,firstN_mtp,firstN_ctp,window_size_sp,window_size_mtp,window_size_ctp,svm_sp_vs_other,svm_mtp_vs_other,svm_ctp_vs_other, svm_sp_vs_mtp,svm_sp_vs_ctp,svm_mtp_vs_sp,svm_mtp_vs_ctp,svm_ctp_vs_sp):

	file = open("%stest_svm1a.dat" % file_path, 'w')

	for i in range (0,len(proteins)):
		pattern = create_pattern(proteins[i]['sequence'],"test",window_size_mtp,firstN_mtp)
		for p in pattern:
			file.write(p)
	file.close()

	if origin == "plant":
		file = open("%stest_svm1b.dat" % file_path, 'w')
		for i in range (0,len(proteins)):
			pattern = create_pattern(proteins[i]['sequence'],"test",window_size_ctp,firstN_ctp)
			for p in pattern:
				file.write(p)
		file.close()

	file = open("%stest_svm1c.dat" % file_path, 'w')
	for i in range (0,len(proteins)):
		pattern = create_pattern(proteins[i]['sequence'],"test",window_size_sp,firstN_sp)
		for p in pattern:
			file.write(p)
	file.close()

	if origin == "plant":
		file = open("%stest_svm1d.dat" % file_path, 'w')
		for i in range (0,len(proteins)):
			pattern = create_pattern2(proteins[i]['sequence'],"0")
			for p in pattern:
				file.write(p)
		file.close()

	os.system(svm_path+"svm-predict -b 1 %stest_svm1a.dat %s %soutput_svm_mtp_vs_other.dat > %sweg" % (file_path,svm_mtp_vs_other,file_path,file_path))
	os.system(svm_path+"svm-predict -b 1 %stest_svm1a.dat %s %soutput_svm_mtp_vs_sp.dat > %sweg" % (file_path,svm_mtp_vs_sp,file_path,file_path))
	if origin == "plant":
		os.system(svm_path+"svm-predict -b 1 %stest_svm1b.dat %s %soutput_svm_ctp_vs_other.dat > %sweg" % (file_path,svm_ctp_vs_other,file_path,file_path))
		os.system(svm_path+"svm-predict -b 1 %stest_svm1b.dat %s %soutput_svm_ctp_vs_sp.dat > %sweg" % (file_path,svm_ctp_vs_sp,file_path,file_path))

	os.system(svm_path+"svm-predict -b 1 %stest_svm1c.dat %s %soutput_svm_sp_vs_other.dat > %sweg" % (file_path,svm_sp_vs_other,file_path,file_path))
	os.system(svm_path+"svm-predict -b 1 %stest_svm1c.dat %s %soutput_svm_sp_vs_mtp.dat > %sweg" % (file_path,svm_sp_vs_mtp,file_path,file_path))
	if origin == "plant":
		os.system(svm_path+"svm-predict -b 1 %stest_svm1c.dat %s %soutput_svm_sp_vs_ctp.dat > %sweg" % (file_path,svm_sp_vs_ctp,file_path,file_path))

		os.system(svm_path+"svm-predict -b 1 %stest_svm1d.dat %s %soutput_svm_mtp_vs_ctp.dat > %sweg" % (file_path,svm_mtp_vs_ctp,file_path,file_path))

	file_output_sp_vs_other = open("%soutput_svm_sp_vs_other.dat" % file_path, 'r')
	file_output_mtp_vs_other = open("%soutput_svm_mtp_vs_other.dat"  % file_path, 'r')
	if origin == "plant":
		file_output_ctp_vs_other = open("%soutput_svm_ctp_vs_other.dat"  % file_path, 'r')
		file_output_mtp_vs_ctp = open("%soutput_svm_mtp_vs_ctp.dat"  % file_path, 'r')
		file_output_sp_vs_ctp = open("%soutput_svm_sp_vs_ctp.dat"  % file_path, 'r')
	file_output_sp_vs_mtp = open("%soutput_svm_sp_vs_mtp.dat"  % file_path, 'r')
	if origin == "plant":
		file_output_ctp_vs_sp = open("%soutput_svm_ctp_vs_sp.dat"  % file_path, 'r')
	file_output_mtp_vs_sp = open("%soutput_svm_mtp_vs_sp.dat"  % file_path, 'r')

	line=file_output_sp_vs_other.readline()
	line=file_output_mtp_vs_other.readline()
	if origin == "plant":
		line=file_output_ctp_vs_other.readline()
		line=file_output_mtp_vs_ctp.readline()
		line=file_output_sp_vs_ctp.readline()
	line=file_output_sp_vs_mtp.readline()
	if origin == "plant":
		line=file_output_ctp_vs_sp.readline()
	line=file_output_mtp_vs_sp.readline()

	for j in range (0,len(proteins)):
		input_file.write(klasse)
		n = 0

		pattern1 = "^0\s|\s.+$"
		pattern2 ="^1\s.+\s"

		if origin == "plant":
			line = file_output_mtp_vs_ctp.readline()
			line = re.sub("\n","",line)
			line = re.sub(" $","",line)
			if not line: val_mtp_vs_ctp=0
			elif line[0] == "0":
				val_mtp_vs_ctp=re.sub(pattern1,"",line)
				val_mtp_vs_ctp=float(val_mtp_vs_ctp)
			else:
				val_mtp_vs_ctp=re.sub(pattern2,"",line)
				val_mtp_vs_ctp=-1.0*float(val_mtp_vs_ctp)
			mtp_ctp_file.write(str(val_mtp_vs_ctp))
			mtp_ctp_file.write("\n")

		N = firstN_mtp
		if origin == "plant":
			N = firstN_ctp
		for i in range (1,N+1):
			n=4*i-4
			if origin == "plant":
				n=8*i-8
			m = n
			if i <=len(proteins[j]['sequence']) and i <= firstN_mtp:
				line = file_output_sp_vs_other.readline()
				line = re.sub("\n","",line)
				line = re.sub(" $","",line)
				if not line: val_sp_vs_other=0
				elif line[0] == "0":
					val_sp_vs_other=re.sub(pattern1,"",line)
					val_sp_vs_other=float(val_sp_vs_other)
				else:
					val_sp_vs_other=re.sub(pattern2,"",line)
					val_sp_vs_other=-1.0*float(val_sp_vs_other)
			else: val_sp_vs_other=0
			val_sp_vs_other=float(val_sp_vs_other)
			if i <= firstN_mtp:
				m = m + 1
				input_file.write(" "+str(m)+":"+str(val_sp_vs_other))

			if i <=len(proteins[j]['sequence']) and i <= firstN_mtp:
				line = file_output_mtp_vs_other.readline()
				line = re.sub("\n","",line)
				line = re.sub(" $","",line)
				if not line: val_mtp_vs_other=0
				elif line[0] == "0":
					val_mtp_vs_other=re.sub(pattern1,"",line)
					val_mtp_vs_other=float(val_mtp_vs_other)
				else:
					val_mtp_vs_other=re.sub(pattern2,"",line)
					val_mtp_vs_other=-1.0*float(val_mtp_vs_other)
			else: val_mtp_vs_other=0
			val_mtp_vs_other=float(val_mtp_vs_other)
			if i <= firstN_mtp:
				m = m + 1
				input_file.write(" "+str(m)+":"+str(val_mtp_vs_other))

			if origin == "plant":
				if i <=len(proteins[j]['sequence']) and i <= firstN_ctp:
					line = file_output_ctp_vs_other.readline()
					line = re.sub("\n","",line)
					line = re.sub(" $","",line)
					if not line: val_ctp_vs_other=0
					elif line[0] == "0":
						val_ctp_vs_other=re.sub(pattern1,"",line)
						val_ctp_vs_other=float(val_ctp_vs_other)
					else:
						val_ctp_vs_other=re.sub(pattern2,"",line)
						val_ctp_vs_other=-1.0*float(val_ctp_vs_other)
				else: val_ctp_vs_other=0
				val_ctp_vs_other=float(val_ctp_vs_other)
				if i <= firstN_mtp:
					m = m + 1
					input_file.write(" "+str(m)+":"+str(val_ctp_vs_other))

			if i <=len(proteins[j]['sequence']) and i <= firstN_mtp:
				line = file_output_sp_vs_mtp.readline()
				line = re.sub("\n","",line)
				line = re.sub(" $","",line)
				if not line: val_sp_vs_mtp=0
				elif line[0] == "0":
					val_sp_vs_mtp=re.sub(pattern1,"",line)
					val_sp_vs_mtp=float(val_sp_vs_mtp)
				else:
					val_sp_vs_mtp=re.sub(pattern2,"",line)
					val_sp_vs_mtp=-1.0*float(val_sp_vs_mtp)
			else: val_sp_vs_mtp=0
			val_sp_vs_mtp=float(val_sp_vs_mtp)
			if i <= firstN_mtp:
				m = m + 1
				input_file.write(" "+str(m)+":"+str(val_sp_vs_mtp))

			if origin == "plant":
				if i <=len(proteins[j]['sequence']) and i <= firstN_mtp:
					line = file_output_sp_vs_ctp.readline()
					line = re.sub("\n","",line)
					line = re.sub(" $","",line)
					if not line: val_sp_vs_ctp=0
					elif line[0] == "0":
						val_sp_vs_ctp=re.sub(pattern1,"",line)
						val_sp_vs_ctp=float(val_sp_vs_ctp)
					else:
						val_sp_vs_ctp=re.sub(pattern2,"",line)
						val_sp_vs_ctp=-1.0*float(val_sp_vs_ctp)
				else: val_sp_vs_ctp=0
				val_sp_vs_ctp=float(val_sp_vs_ctp)
				if i <= firstN_mtp:
					m = m + 1
					input_file.write(" "+str(m)+":"+str(val_sp_vs_ctp))

				if i <=len(proteins[j]['sequence']) and i <= firstN_ctp:
					line = file_output_ctp_vs_sp.readline()
					line = re.sub("\n","",line)
					line = re.sub(" $","",line)
					if not line: val_ctp_vs_sp=0
					elif line[0] == "0":
						val_ctp_vs_sp=re.sub(pattern1,"",line)
						val_ctp_vs_sp=float(val_ctp_vs_sp)
					else:
					   val_ctp_vs_sp=re.sub(pattern2,"",line)
					   val_ctp_vs_sp=-1.0*float(val_ctp_vs_sp)
				else: val_ctp_vs_sp=0
				val_ctp_vs_sp=float(val_ctp_vs_sp)
				if i <= firstN_mtp:
					m = m + 1
					input_file.write(" "+str(m)+":"+str(val_ctp_vs_sp))

			if i <=len(proteins[j]['sequence']) and i <= firstN_mtp:
				line = file_output_mtp_vs_sp.readline()
				line = re.sub("\n","",line)
				line = re.sub(" $","",line)
				if not line: val_mtp_vs_sp=0
				elif line[0] == "0":
					val_mtp_vs_sp=re.sub(pattern1,"",line)
					val_mtp_vs_sp=float(val_mtp_vs_sp)
				else:
					val_mtp_vs_sp=re.sub(pattern2,"",line)
					val_mtp_vs_sp=-1.0*float(val_mtp_vs_sp)
			else: val_mtp_vs_sp=0
			val_mtp_vs_sp=float(val_mtp_vs_sp)
			if i <= firstN_mtp:
				m = m + 1
				input_file.write(" "+str(m)+":"+str(val_mtp_vs_sp))

			if origin == "plant":
				if i <= firstN_mtp:
					m = m + 1
					input_file.write(" "+str(m)+":"+str(val_mtp_vs_ctp))
		input_file.write("\n")


	file_output_sp_vs_other.close()
	if origin == "plant":
		file_output_ctp_vs_other.close()
	file_output_mtp_vs_other.close()
	if origin == "plant":
		file_output_sp_vs_ctp.close()
	file_output_sp_vs_mtp.close()
	file_output_mtp_vs_sp.close()
	if origin == "plant":
		file_output_mtp_vs_ctp.close()
		file_output_ctp_vs_sp.close()

	os.remove("%sweg" % file_path)
	os.remove("%stest_svm1a.dat" % file_path)
	if origin == "plant":
		os.remove("%stest_svm1b.dat" % file_path)
	os.remove("%stest_svm1c.dat" % file_path)
	if origin == "plant":
		os.remove("%stest_svm1d.dat" % file_path)
	os.remove("%soutput_svm_sp_vs_other.dat" % file_path)
	os.remove("%soutput_svm_mtp_vs_other.dat"  % file_path)
	if origin == "plant":
		os.remove("%soutput_svm_ctp_vs_other.dat"  % file_path)
		os.remove("%soutput_svm_mtp_vs_ctp.dat"  % file_path)
		os.remove("%soutput_svm_sp_vs_ctp.dat"  % file_path)
	os.remove("%soutput_svm_sp_vs_mtp.dat"  % file_path)
	if origin == "plant":
		os.remove("%soutput_svm_ctp_vs_sp.dat"  % file_path)
	os.remove("%soutput_svm_mtp_vs_sp.dat"  % file_path)


def predict(origin,data,model,svm_model_path,libsvm_path,id=1):
	global svm_path
	svm_path = libsvm_path
	file_path = tmpfile_path+"/"+str(id)
	model = str(model)

	svm_sp_vs_other = svm_model_path+"/sp_vs_other/%s.model" %(model)
	svm_mtp_vs_other= svm_model_path+"/mtp_vs_other/%s.model" %(model)
	if origin == "plant":
		svm_ctp_vs_other= svm_model_path+"/ctp_vs_other/%s.model" %(model)
	svm_sp_vs_mtp = svm_model_path+"/sp_vs_mtp/%s.model" %(model)
	svm_mtp_vs_sp= svm_model_path+"/mtp_vs_sp/%s.model" %(model)
	if origin == "plant":
		svm_mtp_vs_ctp= svm_model_path+"/mtp_vs_ctp/%s.model" %(model)
		svm_ctp_vs_sp= svm_model_path+"/ctp_vs_sp/%s.model" %(model)
		svm_sp_vs_ctp = svm_model_path+"/sp_vs_ctp/%s.model" %(model)
	svm2=svm_model_path+"/level2_%s/%s.model" %(origin,model)

	result=[]
	proteins = util.parse_fasta_file(data)
	input_file = open("%stest_svm2.dat" % file_path, 'w')
	if origin == "plant":
		mtp_ctp_file = open("%smtp_ctp.dat" % file_path, 'w')

	if origin == "plant":
		create_svm2_input("plant",file_path,input_file,mtp_ctp_file,proteins,"0",firstN_sp,firstN_mtp,firstN_ctp,window_size_sp,window_size_mtp,window_size_ctp,svm_sp_vs_other,svm_mtp_vs_other,svm_ctp_vs_other, svm_sp_vs_mtp,svm_sp_vs_ctp,svm_mtp_vs_sp,svm_mtp_vs_ctp,svm_ctp_vs_sp)
	else:
		create_svm2_input("non-plant",file_path,input_file,None,proteins,"0",firstN_sp,firstN_mtp,firstN_ctp,window_size_sp,window_size_mtp,window_size_ctp,svm_sp_vs_other,svm_mtp_vs_other,None, svm_sp_vs_mtp, None,svm_mtp_vs_sp, None, None)
	input_file.close()
	if origin == "plant":
		mtp_ctp_file.close()

	os.system(svm_path+"svm-predict -b 1 %stest_svm2.dat %s %soutput_svm2.dat > %sweg" % (file_path,svm2,file_path,file_path))
	file_output = open("%soutput_svm2.dat" %file_path, 'r')

	if origin == "plant":
		mtp_ctp_file = open("%smtp_ctp.dat" % file_path, 'r')
	file_output.readline()
	if origin == "plant":
		pattern0 = "^.\s|\s[0-9,e,-.]+\s[0-9,e,-.]+\s[0-9,e,-.]+$"
		pattern1 = "^.\s[0-9,e,-.]+\s|\s[0-9,e,-.]+\s[0-9,e,-.]+$"
		pattern2 ="^.\s[0-9,e,-.]+\s[0-9,e,-.]+\s|\s[0-9,e,-.]+$"
		pattern3 ="^.\s[0-9,e,-.]+\s[0-9,e,-.]+\s[0-9,e,-.]+\s"
	else:
		pattern0 = "^.\s|\s[0-9,e,-.]+\s[0-9,e,-.]+$"
		pattern1 = "^.\s[0-9,e,-.]+\s|\s[0-9,e,-.]+$"
		pattern2 ="^.\s[0-9,e,-.]+\s[0-9,e,-.]+\s"
	for i in range (0,len(proteins)):
		line = file_output.readline()
		line = re.sub("\n","",line)
		line = re.sub(" $","",line)
		if origin == "plant":
			line2 = mtp_ctp_file.readline()
			line2 = re.sub("\n","",line2)
			score_ctp = float(re.sub(pattern0,"",line))
			score_mtp = float(re.sub(pattern1,"",line))
			score_sp = float(re.sub(pattern2,"",line))
			score_other = float(re.sub(pattern3,"",line))
			score_mtp_vs_ctp = float(line2)
			result.append({'id':proteins[i]['id'],'score_mtp':score_mtp,'score_ctp':score_ctp,'score_sp':score_sp,'score_other':score_other,'score_mtp_vs_ctp':score_mtp_vs_ctp})
		else:
			score_mtp = float(re.sub(pattern0,"",line))
			score_sp = float(re.sub(pattern1,"",line))
			score_other = float(re.sub(pattern2,"",line))
			result.append({'id':proteins[i]['id'],'score_mtp':score_mtp,'score_sp':score_sp,'score_other':score_other})
	file_output.close()
	if origin == "plant":
	   mtp_ctp_file.close()

	os.remove("%sweg" % file_path)
	os.remove("%stest_svm2.dat" % file_path)
	os.remove("%soutput_svm2.dat" % file_path)
	if origin == "plant":
		os.remove("%smtp_ctp.dat" % file_path)
	return result

def plant_predict(data,model,svm_model_path,libsvm_path,id=1):
	return predict("plant",data,model,svm_model_path,libsvm_path,id)

def noplant_predict(data,model,svm_model_path,libsvm_path,id=1):
	return predict("noplant",data,model,svm_model_path,libsvm_path,id)
