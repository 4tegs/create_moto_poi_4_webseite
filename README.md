# **create_moto_poi_4_webseite**

## Version and Licence ##

- Version v1.1 dated 12/2024
 Written by Hans Strassguetl - [https://gravelmaps.de](https://gravelmaps.de/)  
 Licenced under [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)  
- Icons used are licensed under  
 Map Icons Collection  
 Creative Commons 3.0 BY-SA  
 Author: Nicolas Mollet  
[https://mapicons.mapsmarker.com](https://mapicons.mapsmarker.com/)  

## About ##

This program pulls exclusevly motorcycle dealer data from OpenStreetMap using the Overpass Turbo API. Pulled data is converted to Points of Interest (POI) or Waypoints 
* in a KML format for Oruxmaps (Standard KML with icons)
* in a KML format for OrganicMaps (Special Icon/Pin treatment)
* GPX for Garmin including Garmin Symbol
* GPI for Garmin Points of Interest (POI including Icon)

All data is queried globally.

## Details for usage ##

Just run the exe.

## Known limitations ##

None

## Data privacy ##

- By design XML structures as GPX and KML reach out for external servers. For example, interpreting the Garmin GPX, you will find certain html addresses in the GPX's header that support interpreting the structure.
- Using icons make the KML interpreter (as Oruxmaps) reaching out to my server via [http://motorradtouren.de/pics](http://motorradtouren.de/pics)
 No access data is collected or stored for this service by this program or on the server motorradtouren.de.
