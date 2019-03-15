import sys, os, re, math


def multiclass_probability(nr_class,pairwise_prob,prob_estimates):
	
	iter = 0
	max_iter=100
	   
	Q=[]
	Qp = []
	pQp = 0.0
	eps = 0.005 / float(nr_class)
	
	for i in range(0,nr_class):
		Q.append([])
		Qp.append(0.0)
		for j in range(0,nr_class):
			Q[i].append(0.0)
	
	for t in range(0,nr_class):
		prob_estimates[t] = 1.0 / float(nr_class)
		Q[t][t] = 0.0
		for j in range(0,t):
			Q[t][t] = Q[t][t] + pairwise_prob[j][t] * pairwise_prob[j][t]
			Q[t][j] = Q[j][t]
		for j in range(t+1,nr_class):
			Q[t][t] = Q[t][t] + pairwise_prob[j][t] * pairwise_prob[j][t]
			Q[t][j] = -pairwise_prob[j][t] * pairwise_prob[t][j]
	
	for iter in range(0,max_iter):
		pQp=0
		for t in range(0,nr_class):
			Qp[t]=0
			for j in range(0,nr_class):
				Qp[t] = Qp[t] + Q[t][j] * prob_estimates[j]
			pQp = pQp + prob_estimates[t] * Qp[t]
		max_error=0.0
		for t in range(0,nr_class):
			error=abs(Qp[t]-pQp)
			if error>max_error:
				max_error=error
		if max_error<eps: break
		for t in range(0,nr_class):
			diff=(-Qp[t]+pQp)/Q[t][t]
			prob_estimates[t] = prob_estimates[t]+ diff
			pQp=(pQp+diff*(diff*Q[t][t]+2.0*Qp[t]))/(1.0+diff)/(1.0+diff)
			for j in range(0,nr_class):
				Qp[j]=(Qp[j]+diff*Q[t][j])/(1.0+diff)
				prob_estimates[j] = prob_estimates[j] / (1.0+diff)
	if iter>=max_iter:
		print "Exceeds max_iter in multiclass_prob"


def estimate(nr_class,probs):
	
	prob_estimates = []
	pairwise_prob = []

	for i in range(0,nr_class):
		prob_estimates.append(0.0)
		pairwise_prob.append([])
		for j in range(0,nr_class):
			pairwise_prob[i].append(0.0)

	l=0
	for i in range(0,nr_class):
		for j in range(i+1,nr_class):
			pairwise_prob[i][j] = float(probs[l])
			if pairwise_prob[i][j] == 1.0:
				pairwise_prob[i][j] = 0.99999
			pairwise_prob[j][i] = 1.0 - pairwise_prob[i][j]
			l = l +1
			
	multiclass_probability(nr_class,pairwise_prob,prob_estimates)

	prob_max_idx = 0
	result = []
	for i in range(1,nr_class):
		if prob_estimates[i] > prob_estimates[prob_max_idx]:
			prob_max_idx = i
	#result.append(prob_max_idx)
	for i in range(0,nr_class):
		result.append(round(prob_estimates[i],6))
	return result

"""
def main():
	nr_class = int(sys.argv[1])
	probs=[]
	for i in range(2,len(sys.argv)):
		probs.append(float(sys.argv[i]))
	result = estimate(nr_class,probs)
	line=""
	for i in range(0,len(result)):
		line= line + str(result[i]) + " "
	print line

main()
"""
