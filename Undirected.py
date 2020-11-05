import pandas as pd
import csv
import networkx as nx 
import matplotlib.pyplot as plt



tem=[]

class GraphVisualization: 

	def __init__(self): 
		
		self.visual = [] 
		
	def addEdge(self, a, b): 
		temp = [a, b] 
		self.visual.append(temp) 
		
	
	def visualize(self): 
		G = nx.Graph() 
		G.add_edges_from(self.visual) 
		nx.draw_networkx(G) 
		plt.show() 

for p in range(1950,1999):
	with open('Table/'+str(p)+'.csv') as csvDataFile:
 		csvReader = csv.reader(csvDataFile)
 		for row in csvReader:
 			tem.append(row)
 	#print(temp)

 		G = GraphVisualization()
 		for i in range(len(tem)):
 			G.addEdge(tem[i][0],tem[i][1])

 		G.visualize()
 		#print(tem)
 		tem.clear() 
