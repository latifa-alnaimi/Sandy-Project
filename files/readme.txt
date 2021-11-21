------------
datacenter:
------------
Contains Location superclass inherited by DataCenter and Station (inherit attributes id, lat & lon)
Coordinates of Stations are obtained from a text file and stored in a dictionary at the start of the module
Station objects are created in "observers" but stored in a dictionary defined and referenced here (stations_dict)


-----------
observers:
-----------

Contains view classes Print and Map
Map is drawn in update() of Map class with current status of data centers and stations
Metar extraction happens in main
	So stations_dict (from datacenter module) is also populated in main (creating Station objects after obtaining metar)

-----
New:
-----
Obtaining data center info from XML file instead of text file (created in a function, called in 'run')