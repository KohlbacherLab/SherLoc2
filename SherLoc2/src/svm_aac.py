import re, os, sys, string, util

tmpfile_path=""

def create_pattern_aac(sequence,klasse):
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

def create_pattern(type,sequence,klasse):
	if type=="aa_pair":
		return create_pattern_aa_pair(sequence,klasse)
	else:
		return create_pattern_aac(sequence,klasse)


def predict(origin,aac_type,table,path,data,model,libsvm_path, id=1):
	model=str(model)

	proteins = util.parse_fasta_file(data)
	no_fv_proteins = []

	file_path = tmpfile_path+"/"+str(id)
	input_file = open("%stest_svm.dat" % file_path, 'w')
	for i in range (0,len(proteins)):
		pattern = create_pattern(aac_type,proteins[i]['sequence'],"0")
		for p in pattern:
			input_file.write(p)
	input_file.close()

	return util.predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins)

def animal_predict(aac_type,table,path,data,model,libsvm_path, id=1):
	return predict("animal",aac_type,table,path,data,model,libsvm_path, id)

def fungi_predict(aac_type,table,path,data,model,libsvm_path, id=1):
	return predict("fungi",aac_type,table,path,data,model,libsvm_path, id)

def plant_predict(aac_type,table,path,data,model,libsvm_path, id=1):
	return predict("plant",aac_type,table,path,data,model,libsvm_path, id)
