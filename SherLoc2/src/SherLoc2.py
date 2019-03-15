import string, sys, os, getopt, smtplib
import cgi,re,time,posix
#sys.path.append( "/share/www/zope/software/Extensions/" );
import epiloc_interface
import dialoc_interface

import time

sherloc2_path="/share/projects/LOC_PRED/WebServices/SherLoc2-online/"
src_path="/share/projects/LOC_PRED/WebServices/SherLoc2-online/src/"
tmpfile_path="/share/projects/LOC_PRED/WebServices/SherLoc2-online/tmp/"
#python_path="/share/opt/x86_64_sl5/bin/" original?
python_path="/share/opt/x86_64_sl5/Python-2.5.2-default/bin/"#from multiloc2

#the following params have to be set manually
perl_path="/share/opt/i386_sl5/perl-5.10.0"
perl5lib_path="/share/opt/i386_sl5/perl-5.10.0/lib:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0/i686-linux:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0/i686-linux/auto:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0"

def create_prediction_id():
	return "SL2" + str(time.time())

def addEmail(self, REQUEST=None):
	request = self.REQUEST;
	prediction_id = request['prediction_id'];
	email = request['email'];
	os.system(python_path + "/python " + src_path + "/sherloc2_add_mail.py "+str(prediction_id)+" "+str(email));
	f = open("%semail_%s.txt" %(tmpfile_path,str(prediction_id)),"r");
	out_string = "";
	line = f.readline();
	while line:
		out_string += line;
		line = f.readline();
	
	f.close();

	os.system("rm %semail_%s.txt" %(tmpfile_path,str(prediction_id)));
	
	return out_string;
	
def getResult(self, REQUEST=None):
	request = self.REQUEST;
	prediction_id = request['prediction_id']
	
	os.system(python_path + "/python " + src_path + "/sherloc2_get_prediction.py "+str(prediction_id));
	f = open("%s/result_%s.txt" %(tmpfile_path,str(prediction_id)),"r");#	f = open("%sresult_%s.txt" %(tmpfile_path,str(prediction_id)),"r");
	out_string = "";
	line = f.readline();
	while line:
		out_string += line;
		line = f.readline();
	
	f.close();

	os.system("rm %s/result_%s.txt" %(tmpfile_path,str(prediction_id)));#	os.system("rm %sresult_%s.txt" %(tmpfile_path,str(prediction_id)));

	return out_string;

def write_epiloc_result_file(prediction_id, epiloc_result_list):
	file_name = tmpfile_path + "/" + prediction_id + "epiloc_result.er"
	f = open( file_name, "w");
	for elem in epiloc_result_list:
		line_string = str(elem["id"]);
		for key in elem.keys():
			if key != "id":
				line_string += " " + str(key) + " " + str(elem[key]);
		f.write(line_string+"\n");
	f.close();

	return file_name;
	

def call_sherloc2(query_file_name, origin, email, prediction_id, epiloc_result_list):
	# write epiloc result into a file
	epiloc_result_file_name = write_epiloc_result_file(prediction_id, epiloc_result_list);
	#save that sherloc2 is used
	stat_file = open(sherloc2_path + "/webservice_stat.txt","a");
	stat_file.write(str(prediction_id)+" "+email+" "+origin+" "+str(len(epiloc_result_list))+"\n");
	stat_file.close();
	
	os.environ["PATH"]=perl_path + ":" + os.environ["PATH"]
	os.environ["PERL5LIB"]=perl5lib_path
	
	os.system(python_path + "/python " + src_path + "/sherloc2_prediction_online.py -fasta="+query_file_name+" -origin="+origin+" -email="+email+" -pid=" + prediction_id + " -rm_fasta=1 -epiloc="+epiloc_result_file_name+" &")
	
def sherloc2(self, REQUEST=None):
	request = self.REQUEST
	pred_method = request['pred_method']
	origin="animal"
	if pred_method=="2":
		origin="fungal"
	elif pred_method=="3":
		origin="plant"

	# check always first if fastafile is set, since the intermediate screen has no fastafile field
	prediction_id = create_prediction_id()
	if "fastafile" in request.keys():
		fastafile = request['fastafile']
	fastapaste = request['fastapaste']
	email = ""
	return_string = ""
	#if email == "":
	#	return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Please enter your email-address!</font></p>"
	if email != "" and len(re.findall("^[\w.-]+@[\w.-]+$",email)) == 0:
		return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: This is not a valid email-address!</font></p>"
	if fastapaste == "":
		if "fastafile" in request.keys():
			if fastafile.filename == "":
				return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Please paste a sequence or specifiy a file with fasta sequences!</font></p>"
		else:
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Please paste a sequence or specifiy a file with fasta sequences!</font></p>"
	
	# !!!!!!!!!!!!! fasta format checker necessary!!!!!!!!!
	query_file_name = tmpfile_path + "/" + prediction_id + "query.fasta"
	if fastapaste != "":
		file = open(query_file_name,"w")
		if len(re.findall(">",fastapaste)) > 20:
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Too many sequences!</font></p>"
		if fastapaste[0] != ">":
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Wrong fasta format!</font></p>"
		tokens = fastapaste.split("\n")
		for token in tokens:
			line = token
			if line == "":
				continue
			if line[0] != ">":
				line=re.sub("\s","",line)
				line=string.upper(line)
			file.write(line + "\n")
		file.close()

	text=""
	if fastapaste == "":
		file = open(query_file_name,"w")
		file_tmp = fastafile
		text = file_tmp.read()
		file_tmp.seek(0)
		if len(re.findall(">",text)) > 20:
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Too many sequences in fasta file!</font></p>"
		line=fastafile.readline()
		if line[0] != ">":
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Wrong fasta format!</font></p>"
		file.write(line)
		fastapaste.append(line);
		while 1:
			line=fastafile.readline()
			if line=="": break
			if line[0]!=">":
				line=re.sub("\s","",line)
				line=string.upper(line)
			file.write(line+"\n")
			fastapaste.append(line+"\n");
		file.close()
	
	return_string = "<p>Your query has been submitted to SherLoc2. Your prediction ID is "+str(prediction_id)+"</p>";
	return_string += "<p>You can access the prediction results on the <a href='http://www-bs4.informatik.uni-tuebingen.de/Services/SherLoc2'>SherLoc2 webpage</a> by entering the prediction ID above or by <a href='http://www-bs4.informatik.uni-tuebingen.de/Services/SherLoc2/sherloc2_getResult?prediction_id="+str(prediction_id)+"'>clicking here.</a></p>";	
		
	return_string += "<p>Alternatively, you may provide an email address below. The prediction results will be send to you as soon as the prediction is finished. </p>";
	return_string += "<form enctype=multipart/form-data action=sherloc2_addEmail method=post>"
	return_string += "<input type=hidden name=prediction_id value='"+str(prediction_id)+"'>";
	return_string += "<input type=text name=email value='' size=30><BR><BR>";
	return_string += "<input type=submit name=Submit value='Submit'><BR>";
	return_string += "</form>";
	
	# after writing the sequences in a file, test whether an epiloc score is obtained already
	if not "sequence1_epiloc_uniform" in request.keys():
	
		# if not, call epiloc with the current settings
		f1 = open(query_file_name,"r");
		epiloc_result = [];
	
		os.environ["http_proxy"]="http://www-cache.informatik.uni-tuebingen.de:3128/"
		
		if origin == "fungal":
			epiloc_result = epiloc_interface.fungi_predict(f1);
		elif origin == "animal":
			epiloc_result = epiloc_interface.animal_predict(f1);
		elif origin == "plant":
			epiloc_result = epiloc_interface.plant_predict(f1);
		else:
			return "<p><font color=\"red\"><span style=\"font-weight:bold\">ERROR: Origin is corrupted!</font></p>"
		f1.close();
	
		# test whether epiloc returned a uniform probability vector for one of the sequences
		uniform_vector = False;
		for protein in epiloc_result:
			if protein["uniform_probabilities"] == 1:
				uniform_vector = True;
		
		dialoc_example="The nucleotide sequences of 21 Pl and TAC clones which have been precisely localized to the fine physical map of the Arabidopsis thaliana chromosome 5, were determined, and their sequence features were analyzed. The total length of the regions sequenced in this study were 1,381,565 bp, bringing the total length of the chromosome 5 sequences determined so far to 6,691,670 bp together with the regions of the 69 clones previously reported. By computer-aided analyses including similarity search against protein and EST databases and gene modeling with computer programs, a total of 337 potential protein-coding genes and/or gene segments were identified on the basis of similarity to the reported gene sequences. An average density of the genes and/or gene segments thus assigned was 1 gene / 4,100 bp. Introns were identified in 76.7% of the potential protein genes for which the entire gene structure were predicted, and the average number per gene and the average length of the introns were 3.9 and 176 bp, respectively. These sequence features are essentially identical to those in the previously reported sequences. The numbers of the Arabidopsis ESTs matched to each of the predicted genes have been counted to monitor the transcription level. The sequence data and gene information are available on the World Wide Web database KAOS (Kazusa Arabidopsis data Opening Site) at http://www.kazusa.or.jp/arabi/.";
		
		# depending on the epiloc results print a intermediate screen, or call sherloc2
		
		if uniform_vector == False:
			call_sherloc2(query_file_name, origin, email, prediction_id, epiloc_result);
		else:
			return_string = "";
			return_string += "<script language='JavaScript'>";
			return_string += "<!--";
			return_string += "function cd()";
			return_string += "{";
			return_string += "alert('hi');";
			return_string += "}";
			return_string += "function checkLength(element)";
			return_string += "{";
			return_string += "var length = element.value.split(' ').length;";
			return_string += "alert(length);";
			return_string += "if (length > 10) return false;";
			return_string += "return true";
			return_string += "}";
			return_string += "//-->";
			return_string += "</script>";
			
			return_string += "<br>";
			return_string += "<div>";
			return_string += "<form name=dialoc enctype=multipart/form-data action=sherloc2_results method=post>";
			return_string += "<input type=hidden name=pred_method value='"+str(request['pred_method'])+"'>";
			#return_string += "<input type=hidden name=fastafile value='"+str(request['fastafile'])+"'>";
			return_string += "<input type=hidden name=fastapaste value='"+str(request['fastapaste'])+"'>";
			return_string += "<input type=hidden name=email value='"+str(email)+"'>";
			return_string += "<table width='100%'>";
			return_string += "<tr><td valign=left>";
			return_string += "For some of your protein sequences EpiLoc could not find homologous proteins. "
			return_string += "However, you can describe these protein(s). <BR>"
			return_string += "DiaLoc allows you to enter your current knowledge about your protein(s) ";
			return_string += "as short abstract.  Please make sure that your text consists of at least 100 words.<BR>";
			return_string += "<a href=\"javascript:document.forms['dialoc'].elements[5].value='"+str(dialoc_example)+"'\">Click here to see an example how a description could look like.</a><BR><BR>";
			return_string += "If you have no information about your protein(s) or you choose to skip ";
			return_string += "this step, press the 'Skip' button or leave the description field blank.<BR><BR>";
			
			#save names and proteins with textbox
			textbox_names = [];
			protein_names = [];
			c=1;
			for protein in epiloc_result:
				if protein["uniform_probabilities"] == 1:
					textbox_names.append("sequence"+str(c)+"_description");
					protein_names.append(protein["id"]);
			
			#make skip button
			return_string += "<input type=submit name=Submit2 value=Skip onClick=\"";
			for elem in textbox_names:
				return_string += "document.forms['dialoc'].elements['"+elem+"'].value='';";
			return_string += "\"><BR>";
			return_string += "</td>";
			return_string += "<td valign=right>";
			return_string += "<img width=200 src='Research/Images/Sherloc2_logo.png'>";
			return_string += "</td>";
			return_string += "</table>";

			c = 1;
			# for every protein which needs description print a textbox, otherwise print epiloc results in hidden inputs
			for protein in epiloc_result:
				if protein["uniform_probabilities"] == 1:
					return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_uniform value='1'>"; 
					return_string += "<br>Please describe the protein with ID <i>"+str(protein["id"])+"</i>:<br>";
					return_string += "<textarea name=sequence"+str(c)+"_description cols=50 rows=10></textarea><br>";
				else:
					return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_uniform value='0'>"; 
				
				return_string += "<input type=hidden name=sequence"+str(c)+"_id value='"+str(protein['id'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_nuc value='"+str(protein['score_nuc'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_cyt value='"+str(protein['score_cyt'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_mit value='"+str(protein['score_mit'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_er value='"+str(protein['score_er'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_pm value='"+str(protein['score_pm'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_per value='"+str(protein['score_per'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_gol value='"+str(protein['score_gol'])+"'>"; 
				return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_ext value='"+str(protein['score_ext'])+"'>";
				if origin == "fungal" or origin == "plant":
					return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_vac value='"+str(protein['score_vac'])+"'>"; 
				elif origin == "animal":
					return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_lys value='"+str(protein['score_lys'])+"'>"; 
				if origin == "plant":
					return_string += "<input type=hidden name=sequence"+str(c)+"_epiloc_score_chl value='"+str(protein['score_chl'])+"'>"; 
				c += 1;
				
			return_string += "<input type=submit name=Submit value=Predict onClick=\"";
			for i in range(len(textbox_names)):
				elem = textbox_names[i];
				p = protein_names[i];
				return_string += "if (document.forms['dialoc'].elements['"+elem+"'].value.split(' ').length < 20 && document.forms['dialoc'].elements['"+elem+"'].value.split(' ').length > 1) { alert('Warning! The description of protein "+str(p)+" is too short.  We recommend a text that is between 20 and 150 words. To skip the description of this protein, leave the text box blank.'); return false; }";
			return_string += "return true;";
			return_string += "\">";
			return_string += "<br>";
			return_string += "</form>";
			return_string += "</div>";

	else:
		c = 1;
		final_epiloc_result_list = [];
		dialoc_list = [];
		while "sequence"+str(c)+"_epiloc_uniform" in request.keys():
			# if epiloc was succesful...save it
			if request["sequence"+str(c)+"_epiloc_uniform"] == "0":
				epiloc_results = {};
				epiloc_results["id"] = request["sequence"+str(c)+"_id"];
				epiloc_results["score_nuc"] = request["sequence"+str(c)+"_epiloc_score_nuc"];
				epiloc_results["score_cyt"] = request["sequence"+str(c)+"_epiloc_score_cyt"];
				epiloc_results["score_mit"] = request["sequence"+str(c)+"_epiloc_score_mit"];
				epiloc_results["score_er"] = request["sequence"+str(c)+"_epiloc_score_er"];
				epiloc_results["score_pm"] = request["sequence"+str(c)+"_epiloc_score_pm"];
				epiloc_results["score_per"] = request["sequence"+str(c)+"_epiloc_score_per"];
				epiloc_results["score_gol"] = request["sequence"+str(c)+"_epiloc_score_gol"];
				epiloc_results["score_ext"] = request["sequence"+str(c)+"_epiloc_score_ext"];
				if origin == "fungal" or origin == "plant":
					epiloc_results["score_vac"] = request["sequence"+str(c)+"_epiloc_score_vac"];
				elif origin == "animal":
					epiloc_results["score_lys"] = request["sequence"+str(c)+"_epiloc_score_lys"];
				if origin == "plant":
					epiloc_results["score_chl"] = request["sequence"+str(c)+"_epiloc_score_chl"];
				final_epiloc_result_list.append(epiloc_results);
			else:
				# if no description was entered....save it
				if request["sequence"+str(c)+"_description"] == "" or request["Submit"] == "Skip":
					epiloc_results = {};
					epiloc_results["id"] = request["sequence"+str(c)+"_id"];
					epiloc_results["score_nuc"] = request["sequence"+str(c)+"_epiloc_score_nuc"];
					epiloc_results["score_cyt"] = request["sequence"+str(c)+"_epiloc_score_cyt"];
					epiloc_results["score_mit"] = request["sequence"+str(c)+"_epiloc_score_mit"];
					epiloc_results["score_er"] = request["sequence"+str(c)+"_epiloc_score_er"];
					epiloc_results["score_pm"] = request["sequence"+str(c)+"_epiloc_score_pm"];
					epiloc_results["score_per"] = request["sequence"+str(c)+"_epiloc_score_per"];
					epiloc_results["score_gol"] = request["sequence"+str(c)+"_epiloc_score_gol"];
					epiloc_results["score_ext"] = request["sequence"+str(c)+"_epiloc_score_ext"];
					if origin == "fungal" or origin == "plant":
						epiloc_results["score_vac"] = request["sequence"+str(c)+"_epiloc_score_vac"];
					elif origin == "animal":
						epiloc_results["score_lys"] = request["sequence"+str(c)+"_epiloc_score_lys"];
					if origin == "plant":
						epiloc_results["score_chl"] = request["sequence"+str(c)+"_epiloc_score_chl"];
					final_epiloc_result_list.append(epiloc_results);
				else:
					# otherwise save that dialoc needs to be called
					dialoc_results = dialoc_interface.predict(request["sequence"+str(c)+"_id"], request["sequence"+str(c)+"_description"], origin);
					final_epiloc_result_list.append(dialoc_results);
					dialoc_list.append(c-1);
			c += 1;	
		
		# after constructing the result list call SherLoc2 for the final prediction
		call_sherloc2(query_file_name, origin, email, prediction_id, final_epiloc_result_list);
		#return_string += str(final_epiloc_result_list);
		
	return return_string;
	"""
	return_string = "<p>The prediction results will be send to " + email + "</p><br>" + "<p>If you will not recieve the results within 24 hours, please let us know or resubmit your query!</p>"
	
	os.environ["PATH"]="/share/opt/i386_sl5/perl-5.10.0:" + os.environ["PATH"]
	os.environ["PERL5LIB"]="/share/opt/i386_sl5/perl-5.10.0/lib:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0/i686-linux:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0/i686-linux/auto:/share/opt/i386_sl5/perl-5.10.0/lib/perl5/5.10.0"
	os.system("/share/opt/i386_rh90/bin/python /share/projects/LOC_PRED/WebServices/python/SherLoc2/sherloc2_prediction.py -fasta="+query_file_name+" -origin="+origin+" -email="+email+" -pid=" + prediction_id + " -rm_fasta=1 &")
	
	return return_string
	"""
