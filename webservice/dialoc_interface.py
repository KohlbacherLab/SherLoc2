import urllib2;
import urllib;
import socket;
import re;

# DIALOC interface script, 2009 Sebastian Briesemeister
# This script aims as interface between ML2 and DiaLoc.
# The functions plant_predict, animal_predict, and fungi_predict
# are the public functions that take a file stream as input and
# return a list of predictions. Each lists contains the id of the
# protein in the fasta file and the scores of the locations of this
# species.
# The script uses the http protocol, so make sure the connection
# is not blocked.
# For details see comments.

# global definition of DiaLoc webpage
dialoc_url = "http://epiloc.cs.queensu.ca/cgi-bin/brady/predict.pl";

output_translation = { "chloroplast" : "score_chl", "vacuolar" : "score_vac", "mitochondrial" : "score_mit",
	"cytoplasmic" : "score_cyt", "extracellular" : "score_ext", "Golgi_apparatus" : "score_gol" , "ER" : "score_er",
	"plasma_membrane" : "score_pm", "lysosomal" : "score_lys", "nuclear" : "score_nuc", "peroxisomal" : "score_per"};


# DiaLoc request function needs a aa sequence, and the name of an organism
# Swiss_prot_ac is optional. It uses the DiaLoc web interface to
# receive the prediction probabilities of DiaLoc.
def __request(aasequence, organism, swiss_prot_ac = ""):
	# standard output = dictionary of probabilities
	# initiated with zero
	dialoc_output = { "score_nuc" : 0, "score_cyt" : 0, "score_vac" : 0, "score_pm" : 0, "score_lys" : 0, "score_per" : 0,
			"score_mit" : 0, "score_chl" : 0, "score_gol" : 0, "score_er" : 0, "score_ext" : 0};

	# set organism id as specified in DiaiLoc
	organism_id = 0;
	if organism == "animal":
		organism_id = 1;
		del dialoc_output["score_chl"];
		del dialoc_output["score_vac"];
	elif organism == "fungal":
		organism_id = 2;
		del dialoc_output["score_chl"];
		del dialoc_output["score_lys"];
	elif organism == "plant":
		organism_id = 3;
		del dialoc_output["score_lys"];
	else:
		throw("DiaLoc.py:  Unknown organism '"+str(organism)+"'!");


	# set up a dictionary with the post form variables
	dialoc_input = { "description" : str(aasequence),
		"pred_method" : str(organism_id) };


	# call DiaLoc via http and retrieve webpage
	data = urllib.urlencode(dialoc_input);
	req = urllib2.Request(dialoc_url, data);
	response = urllib2.urlopen(req, timeout=10);
	webpage = response.read();


	# check first whether there was an error
	# if so output zero probability vector
	re_res = re.findall("Unable to determine location with provided information", webpage);
	if len(re_res) > 0:
		return dialoc_output;


	# parse webpage and retrieve probabilites for every location
	# save probabilities in dictionary
	re_res = re.findall("<tr><td align=center>.{1,15}</td><td align=center>.{2,10}</td></tr>", webpage);
	for location in re_res:
		loc_name = re.findall(">.{1,15}</td><td", location);
		loc_name = loc_name[0][1:loc_name[0].rfind("</td")];
		loc_prob = re.findall(">.{2,10}</td></tr>", location);
		loc_prob = loc_prob[0][1:loc_prob[0].rfind("</td")];
		dialoc_output[output_translation[loc_name]] = loc_prob;


	# return probability dictionary
	return dialoc_output;


def predict(id,protein_description, organism):
	# contact dialoc
	dialoc_output = __request(protein_description, organism, id);
	# test whether everything is zero and no prediction was returned
	zero = True;
	for elem in dialoc_output.keys():
		if dialoc_output[elem] != 0:
			zero = False;
	# ..if so..set uniform probabilities
	#dialoc_output["uniform_probabilities"] = 0;
	if zero:
		for elem in dialoc_output.keys():
			dialoc_output[elem] = 1.0/len(dialoc_output.keys());
		#dialoc_output["uniform_probabilities"] = 1;
	# add id and final dictionary to output list
	dialoc_output["id"] = id;
	return dialoc_output;



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
