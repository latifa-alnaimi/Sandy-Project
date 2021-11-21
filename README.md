# Storm Finder Project

### Objectives
1. Detect storms approaching data centers
2. Classify critical statuses of data centers 
3. Take action to migrate traffic to less critical centers


### Process
1. Extract weather information from METAR file, a standardized weather reporting format. Example format:
    ```
    KTEB 300000Z 09037G53KT 5SM RA BR SCT025 OVC036 17/13 A2862
    KMMU 042345Z 35005KT 10SM OVC048 06/M01 A2999
    ```
2. Update status of weather stations based on weather information. Color codes: Green &rarr; safe, Yellow &rarr; warning, Red &rarr; storm very likely
3. Get nearby stations that would affect data centers.
4. Update status of data centers.


