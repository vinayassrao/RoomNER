import plac
import spacy
import pandas as pd
import os
import re



@plac.annotations(model=("Model name. Defaults to blank 'en' model.", "option", "m", str) )


def main(model=None):
	ROOM =[]
	temp =[]
	temp1 =[]
	temp2 =[]
	p=1950
	nlp = spacy.load(model)#Loading the model which was trained Train.py
	print("Loaded model '%s'" % model)

	if not os.path.exists('Table'):
		os.makedirs('Table')

	all_files = os.listdir("plan50")       #Opening the folder containing test data,this statement creates list of all text file in the directory plan50
	#print(all_files)   
	for txt in all_files:     
		temp1.clear()
		ROOM.clear()
		temp.clear()
		#print(temp1)
		print("TEST DATA : ",p-1949)            #Reading and processing from each of the test text files for processing.
		txt_dir = "plan50/" + txt
		with open(txt_dir, 'r') as txt_file:
			con=txt_file.read()                                               #Remove Stop words from ent.text
			#print(con)                                                       #tokenize to words
			doc = nlp(con)
			#print(con)                                                    #COmpare with'ROOM' and create an array and dataframe it                             
			#print("Entities in '%s'" % con)
			for ent in doc.ents:
				temp.clear()
				if ent.label_ == 'ROOM':
					ROOM.append(ent.text)
					#print(ROOM)
				if ent.label_ == 'CONNECTION' :

					
					print(ent.label_,ent.text)
					for i in range(len(ROOM)):
						if re.search(r'\b'+ROOM[i]+r'\b',ent.text) and ROOM[i] not in temp : 
							temp.append(ROOM[i])
							#print(ROOM[i])
							#print(temp)
					
								
					#if (re.search(r'\bnext to\b',ent.text) or re.search(r'\badjacent to\b',ent.text)) == True:
					if (ent.text.find('adjacent') != -1) or (ent.text.find('next') != -1): 
						#print(ent.text)	
						first_word = ent.text.split()[0]
						for u in range(len(temp)):
							if re.search(r'\b'+temp[u]+r'\b',ent.text):
								if first_word != temp[u] :
									if ([first_word,temp[u]] not in temp1) and ([temp[u],first_word] not in temp1):
										temp1.append([first_word,temp[u]])
						#print(temp1)
						#temp.append(ROOM[i])
						#temp.remove(first_word) 

					else :
						for k in range(len(temp)):
							for j in range(k+1,len(temp)):
								if (([temp[k],temp[j]]) not in temp1) and (([temp[j],temp[k]]) not in temp1):
									temp1.append([temp[k],temp[j]])
									#print(temp1)
									#print(temp1)
						

						
					#temp2=temp2.append(temp1)
					


			print()
			#print(temp1)
		df = pd.DataFrame(temp1, columns = ['Connection', 'Link Type'])
		#print(df)
		df.to_csv('Table/'+str(p)+'.csv', header=True, index=False)
		df.drop(df.index, inplace=True)
		#print()
		#print(df)

				
			
		p=p+1
if __name__ == '__main__':
	plac.call(main)
