import pandas as pd
import re
from collections import defaultdict
from math import sqrt
import random
import time
import os.path
import csv

def densify(x, n):
	d = [0] * n
	for i, v in x:
		d[i] = v
	return d


def eucl_dist(x, c):
	sqdist = 0.
	for i, v in x:
		sqdist += (v - c[i]) ** 2
	return sqrt(sqdist)

def cos_sim(a , b):

	s = sum([v*b[i] for (i,v) in a])
	A =sqrt(sum([e*e for (_,e) in a]))
	B = sqrt(sum([e*e for e in b]))

	return s/(A*B)

def mean(xs, l):
	c = [0.] * l
	n = 0
	for x in xs:
		for i, v in x:
			c[i] += v
		n += 1
	for i in range(l):
		c[i] /= n
	return c

def writeCSV(clusters, articles):
	if os.path.exists("./clustering_KMeans.csv") == True:
		os.remove("./clustering_KMeans.csv")

	file = open("./clustering_KMeans.csv", 'wt')
	writer = csv.writer(file)
	writer.writerow( ('', 'Politics', 'Business', 'Football', 'Film', 'Technology') )

	j = 0
	print len(clusters)
	for c in clusters:
		j+=1
		pol = 0
		buis = 0
		foot = 0
		film = 0
		tech = 0
		print c
		clusterSize = clusters[c]
		#clustSize = len(c)
		for i in clusters[c]:
			if(articles["Category"][i] == "Politics") : pol +=1
			elif(articles["Category"][i] == "Business") : buis +=1
			elif(articles["Category"][i] == "Football") : foot +=1
			elif(articles["Category"][i] == "Film") : film +=1
			elif(articles["Category"][i] == "Technology") : tech +=1
			else : print("Unknown Cat : "+articles[i]["category"])
		pol = pol/clustSize
		buis = buis/clustSize
		foot = foot/clustSize
		film = film/clustSize
		tech = tech/clustSize
		clusterName = "Cluster " + str(j) + " (Size: " + str(clustSize) + ")" 
		writer.writerow( (clusterName, pol, buis, foot, film, tech) )
	file.close()

def comp(l1, l2):
	s1 = set(map(tuple, l1))
	s2 = set(map(tuple, l2))
	if len(s1.symmetric_difference(s2)) == 0:
		return True
	return False

def kmeans(k, xs, l, data , dist_func='eucl_dist' ):
	centers = [densify(xs[i], l) for i in random.sample(range(len(xs)), k)]
	cluster = [None] * len(xs)
	start_time = time.time()
	prev_time = start_time

	iteration= 0
	old_clusters = None
	while True:

		new_time = time.time()
		loop_time = new_time - prev_time
		prev_time = new_time
		print("Iter : %i (%.2f s)" % (iteration , loop_time) )

		for i, x in enumerate(xs):
			if dist_func == 'eucl_dist':
				cluster[i] = min(range(k), key=lambda j: eucl_dist(xs[i], centers[j]))
			elif dist_func == 'cos_sim':
				cluster[i] = max(range(k), key=lambda j: cos_sim(xs[i], centers[j]))

		clusters = [set() for _ in range(k)]
		for i, j in enumerate(cluster):
			clusters[j].add(i)
		clusterEval(clusters , data)

		change = False
		for i in range(len(clusters)):
			if old_clusters is not None:
				print ("Cluster %d :  old %d - new %d" % (i , len(old_clusters[i]) , len(clusters[i])))
				if len(old_clusters[i]) != len(clusters[i]):
					change = True
					break
			else:
				change = True
				break
		if change == False:
			if comp(clusters, old_clusters) == True:
				break

		for j, c in enumerate(centers):
			members = (x for i, x in enumerate(xs) if cluster[i] == j)
			centers[j] = mean(members, l)

		old_clusters = clusters
		iteration += 1
		if iteration >= 1:
			break
	end_time = time.time()
	print("Done in %.2f s" %(end_time - start_time))

	return cluster

def clusterEval(clusters , articles):
	for c in clusters:
		pol = 0
		buis = 0
		foot = 0
		film = 0
		tech = 0
		clustSize = len(c)
		for i in c:
			if(articles["Category"][i] == "Politics") : pol +=1
			elif(articles["Category"][i] == "Business") : buis +=1
			elif(articles["Category"][i] == "Football") : foot +=1
			elif(articles["Category"][i] == "Film") : film +=1
			elif(articles["Category"][i] == "Technology") : tech +=1
			else : print("Unknown Cat : "+articles[i]["category"])
		print("CLUSTER : ("+str(len(c))+")")
		print("\tPolitics :\t%.2f %%" % ((pol/clustSize)*100))
		print("\tBuisness :\t%.2f %%" % ((buis/clustSize)*100))
		print("\tFootball :\t%.2f %%" % ((foot/clustSize)*100))
		print("\tFilm :\t\t%.2f %%" % ((film/clustSize)*100))
		print("\tTechnology :\t%.2f %%" % ((tech/clustSize)*100))

if __name__ == '__main__':
	data = pd.read_csv('train_set.csv',sep='\t')
	data['Content'] += " " + data['Title']
	text=data['Content']


	vocab = {}
	xs = []

	k=5

	for t in text:
		x = defaultdict(float)

		for w in re.findall(r"\w+", t):
			vocab.setdefault(w, len(vocab))
			x[vocab[w]] += 1
		xs.append(x.items())

	clusters = kmeans(k, xs, len(vocab) , data , dist_func = 'cos_sim')
	print len(clusters)
	print("edw reeeee")
	writeCSV(clusters, data)
