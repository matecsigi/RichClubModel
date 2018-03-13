# RichClubModel
A model that can adjust the rich-club distribution of the generated networks by tuning a single threshold parameter.
### Project description
The model was published in Nature, Scientific Reports: https://www.nature.com/articles/s41598-017-01824-y
### Usage
The model is implemented in the model.py file. The script can be run with the command:
'''
python model.py 500 5
'''
where the firts argument is the number of nodes and the second argument is the threshold for the distance. The average degree is set to 3 and the radius of the disk is set to 10 by deafult.
The program generates the rich-club distribution of the generated network and saves the network in gml format.