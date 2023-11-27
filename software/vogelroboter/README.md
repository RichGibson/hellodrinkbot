# Vögelroboter

The bird quiz robot


## Electronics

- Raspberry pi
- Motor hat
- two peristaltic pumps
- 12 volt power for pumps
- 5 volt power for Raspberry Pi

## Case 

- Some sort of cute bird 
- Somewhere to mount the raspberry pi and two pumps.  
  Various samples and laser cuttable pattern in hellodrinkbot/hardware 
  [Basic Box](../../hardware/basic_box)

## Sofware

- Either add a monitor and keyboard to the Raspberry pi, or connect a 
  tablet or laptop to the raspberry pi via wifi. The raspberry pi will run
  an open Wifi access point with a python-flask app serving the bird quiz. 

## About the Birds

The images of birds should be downloaded and copied to static/birds. The bird 
images are all from Wikipedia, see bird_list.csv for the name of each bird file 
and the link to the wikipedia page for each image with the full attribution 
and licensing details.

## Sounds? (a stretch goal!)

- The raspberry pi has an audio output. If you add speakers the bot could
  play bird songs. See examples of playing sounds  in the [Bender bot](../bender/README.md)
