# RoomNER
A custom based NER for typess of Room,also you can visulaize the connected rooms in the form of  a connected graphs based on information extracted from room plan.


1. To Convert the json data to spacy format(list) use Convert.py with the command, 
								       python Convert.py -i json_file_name -o output_dir

2. Copy the above converted data to the "TRAIN_DATA" variable in Train.py or read the text file where the converted data was stored.

3. Add the new labels in "LABEL = [ ]" in Train.py 

4. To train a new model with 100 iterations use the command,
     						     python Train.py -o output_dir -n 100
   To load from a existing model use the command,
					   python Train.py -m model_name
		    
   You can change number of iterations as you want.If number of iterations is not mentioned by deafult 10 iterations are performed.

5. After training the model, we can perform the testing the process,the test data is loaded from a directory full of text files, use the command,
													                       python Test.py -m model_name
6. Finally to represent the entities in the form of a graph use the Undirected.py use the command,
										    python Undirected.py


  You can change the Dataset depending on your requirement.  
  Just use Convert.py to convert the data in json format to spacy format and then run Train.py to perform custom named entity recognition and save the model.This saved                                                  model can be used to perform operations depending on your requirement.
