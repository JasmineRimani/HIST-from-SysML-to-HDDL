Validation Dynamic Model using the 7 Gb bag 
The model is far from perfect! Please work a bit more on it as soon as you have time!
Really - look in detail into https://www.researchgate.net/publication/288641528_Dynamic_modelling_of_planetary_rovers
Remember that you used the data from the previous paper for the slip defition
For now the main model is the NASA Ames one --> However, there is a lot of parameter identification work that you didn't do totally correctly - PLEASE IMPROVE!

File in this folder:
process_bag_file.py --> A routine to process the bag file you have! Please take the "traslated bag" from https://github.com/AtsushiSakai/rosbag_to_csv
Dynamic_model_Ames_v2_validation.py --> First Validation --> it's kind of ok

Comments:
In general the test of the bag was very bad - I will try to get nice testing from the 07/12 and 09/12 testing. 
The nice test are: (i) go to one point using the navigation stack with a turn, (ii) go straigth using the navigation stack
The test should be short and on point. 

Probably you should give a look to this papers to improve the model:
- ANTARCTICA ROVER DESIGN AND OPTIMIZATION FOR LIMITED POWER CONSUMPTION
- https://www.researchgate.net/publication/288641528_Dynamic_modelling_of_planetary_rovers (Genta)
