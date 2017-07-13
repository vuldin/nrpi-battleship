# nrpi-battleship
*Node-RED-Pi-Battleship*

This app builds on the work done in [SenseHAT_Battleships](https://github.com/TeCoEd/SenseHAT_Battleships).

## Updates
[SenseHAT_Battleships](https://github.com/TeCoEd/SenseHAT_Battleships) was a good starting point, but we wanted a few different features.
Some changes up to this point are:
- remove finding ammo
- add multiplayer
- improve boat representation placement
- improve the rendering of correct pixel state
- database persistence

## Node-RED
*This code is not yet in this repo*

[Node-RED](https://nodered.org/) provides the server, which in turn provides the following features:
- where each player's boats are placed
- collecting shot coordinates from each player
- persisting these shot coordinates in [dashDB](https://www.ibm.com/analytics/us/en/technology/cloud-data-services/dashdb/)
- sending shot result (hit or miss) to the attacker and defender

## Dashboard
*This code is not yet in this repo*

The dashboard reads the [dashDB](https://www.ibm.com/analytics/us/en/technology/cloud-data-services/dashdb/)

## Usage
###
```bash
pip install pygame requests
git clone https://github.com/vuldin/nrpi-battleship.git
cd nrpi-battleship
./runmain.sh
```
The `runmain.sh` script will attempt to start the python app as root using sudo.
This is done since the app needs to initialize the pygame display within a framebuffer.
