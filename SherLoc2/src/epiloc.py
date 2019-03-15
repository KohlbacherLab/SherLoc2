import urllib2;
import urllib;
import socket;
import re;
import util;

# EPILOC interface script, 2009 Sebastian Briesemeister
# This script aims as interface between ML2 and EpiLoc.
# The functions plant_predict, animal_predict, and fungi_predict
# are the public functions that take a file stream as input and
# return a list of predictions. Each lists contains the id of the
# protein in the fasta file and the scores of the locations of this
# species.
# The script uses the http protocol, so make sure the connection
# is not blocked.
# For details see comments.

# global definition of EpiLoc webpage
epiloc_url = "http://epiloc.cs.queensu.ca/cgi-bin/brady/EpiLoc/webpredict.pl";

output_translation = { "chloroplast" : "score_chl", "vacuolar" : "score_vac", "mitochondrial" : "score_mit",
	"cytoplasmic" : "score_cyt", "extracellular" : "score_ext", "Golgi_apparatus" : "score_gol" , "ER" : "score_er",
	"plasma_membrane" : "score_pm", "lysosomal" : "score_lys", "nuclear" : "score_nuc", "peroxisomal" : "score_per"};


# EpiLoc request function needs a aa sequence, and the name of an organism 
# Swiss_prot_ac is optional. It uses the EpiLoc web interface to
# receive the prediction probabilities of EpiLoc.
def __request(aasequence, organism, swiss_prot_ac = ""):

	# standard output = dictionary of probabilities
	# initiated with zero
	epiloc_output = { "score_nuc" : 0, "score_cyt" : 0, "score_vac" : 0, "score_pm" : 0, "score_lys" : 0, "score_per" : 0,
			"score_mit" : 0, "score_chl" : 0, "score_gol" : 0, "score_er" : 0, "score_ext" : 0};

	# set organism id as specified in EpiLoc
	organism_id = 0;
	if organism == "animal":
		organism_id = 1;
		del epiloc_output["score_chl"];
		del epiloc_output["score_vac"];
	elif organism == "fungi":
		organism_id = 2;
		del epiloc_output["score_chl"];
		del epiloc_output["score_lys"];
	elif organism == "plant":
		organism_id = 3;
		del epiloc_output["score_lys"];
	else:
		throw("EpiLoc.py:  Unknown organism '"+str(organism)+"'!");
	
	
	# set up a dictionary with the post form variables
	epiloc_input = { "description" : str(aasequence),
		"pred_method" : str(organism_id),
		"ACC" : str(swiss_prot_ac) };
		
	
	# call EpiLoc via http and retrieve webpage
	data = urllib.urlencode(epiloc_input);
	req = urllib2.Request(epiloc_url, data);
	response = urllib2.urlopen(req);
	webpage = response.read();
		
		
	# check first whether there was an error
	# if so output zero probability vector
	re_res = re.findall("Could not make a prediction", webpage);
	if len(re_res) > 0:
		return epiloc_output;
	
	
	# parse webpage and retrieve probabilites for every location
	# save probabilities in dictionary
	re_res = re.findall("<tr><td align=center>.{1,15}</td><td align=center>.{2,10}</td></tr>", webpage);
	for location in re_res:
		loc_name = re.findall(">.{1,15}</td><td", location);
		loc_name = loc_name[0][1:loc_name[0].rfind("</td")];
		loc_prob = re.findall(">.{2,10}</td></tr>", location);
		loc_prob = loc_prob[0][1:loc_prob[0].rfind("</td")];
		epiloc_output[output_translation[loc_name]] = loc_prob;
		
		
	# return probability dictionary
	return epiloc_output;

	
# gets a filestream as input and returns an epiloc result list
# if the file has wrong format it throws an error
def __parse_epiloc_file(fs, organism):
	animal_keys = ["score_nuc", "score_cyt", "score_pm" , "score_lys" , "score_per" ,
			"score_mit" ,  "score_gol" , "score_er" , "score_ext" ];
	fungi_keys = ["score_nuc", "score_cyt","score_vac", "score_pm" , "score_per" ,
			"score_mit" ,  "score_gol" , "score_er" , "score_ext" ];
	plant_keys = ["score_nuc", "score_cyt","score_vac", "score_pm" , "score_per" ,
			"score_mit" , "score_chl" , "score_gol" , "score_er" , "score_ext" ];
			
	line = fs.readline();
	result_list = [];
	# read in line after line, every line is one dictionary
	while line:
		line_s = line.strip(" \n\r\t").split(" ");
		if len(line_s) == 0:
			raise Error("wrong format in epiloc result file %s!" % fs)
		one_result = {};
		one_result["id"] = line_s[0];
		if (len(line_s) - 1) % 2 != 0:
			raise Error("wrong format in epiloc result file %s!" % fs)
		for c in range( ((len(line_s)-1) / 2)):
			one_result[str(line_s[2*c+1])] = float(line_s[2*c+2]);
		# check whether the keys are correct
		correct = True;
		if organism == "animal":
			for key in animal_keys:
				if not key in one_result.keys():
					correct = False;
		elif organism == "fungi":
			for key in fungi_keys:
				if not key in one_result.keys():
					correct = False;
		elif organism == "plant":
			for key in plant_keys:
				if not key in one_result.keys():
					correct = False;
		if not correct:
			raise Error("wrong format in epiloc result file %s!" % fs)
		
		result_list.append(one_result);
		line = fs.readline();
		
	return result_list;	
	
def __predict(fastafile_stream, organism, epilocfile_stream =  None):
	# check if epiloc file is present
	if epilocfile_stream != None:
		result = __parse_epiloc_file(epilocfile_stream, organism);
		return result;
	
	# get fasta file as list of dictionaries
	proteins = util.parse_fasta_file(fastafile_stream);
	result = [];
	# get predictions for all proteins
	for protein in proteins:
		# contact epiloc
		epiloc_output = __request(protein["sequence"],organism,protein["id"]);
		# test whether everything is zero and no prediction was returned
		zero = True;
		for elem in epiloc_output.keys():
			if epiloc_output[elem] != 0:
				zero = False;
		# ..if so..set uniform probabilities
		if zero:
			for elem in epiloc_output.keys():
				epiloc_output[elem] = 1.0/len(epiloc_output.keys());
		# add id and final dictionary to output list
		epiloc_output["id"] = protein["id"];
		result.append(epiloc_output);
	return result;
	
def plant_predict(fastafile_stream, epilocfile_stream =  None):
	return __predict(fastafile_stream,"plant", epilocfile_stream);
		
def animal_predict(fastafile_stream, epilocfile_stream =  None):
	return __predict(fastafile_stream,"animal", epilocfile_stream);
		
def fungi_predict(fastafile_stream, epilocfile_stream =  None):
	return __predict(fastafile_stream,"fungi", epilocfile_stream);


	
# help and example output of script
"""
print("Hello, this is the EpiLoc-MultiLoc interface.");
print("---------------------------------------------");
print("It will connect to EpiLoc via the Internet and");
print("retrieves the probability output of EpiLoc.");
print("Here example nr 1:");

seq = "MTMDKSELVQKAKLAEQAERYDDMAAAMKAVTEQGHELSNEERNLLSVAYKNVVGARRSSWRVISSIEQKTERNEKKQQMGKEYREKIEAELQDICNDVLELLDKYLIPNATQPESKVFYLKMKGDYFRYLSEVASGDNKQTTVSNSQQAYQEAFEISKKEMQPTHPIRLGLALNFSVFYYEILNSPEKACSLAKTAFDEAIAELDTLNEESYKDSTLIMQLLRDNLTLWTSENQGDEGDAGEGEN";
org = "animal"

print("\t Sequence: "+seq);
print("\t Organism: "+org);
print("...call EpiLoc...");

res = request(seq,org);

print("Output of EpiLoc as python dictionary:");
print("\t "+str(res));
print("\nExample nr 2 will cause an error in EpiLoc:");

seq = "AAAAAAACCCCCCTTTTTTGGGGG";
org = "fungi"

print("\t Sequence: "+seq);
print("\t Organism: "+org);
print("...call EpiLoc...");

res = request(seq,org);
print("Output of EpiLoc as python dictionary:");

print("\t "+str(res));
"""






