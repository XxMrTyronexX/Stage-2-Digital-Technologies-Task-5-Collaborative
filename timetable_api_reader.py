import requests
import json
import os
import re
import linecache
import io

#putting URL containing bus data inside of requests object
r = requests.get("https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions/debug")

#extracting the bus timetable data from the object as a string
response = r.text

#getting the lines of the string returned
lines_of_response = io.StringIO(response).readlines()

#creating blank variables to be concatinated or iterated on
full_text = ""
i = 1

#looping through each line of the bus schedule
for line in lines_of_response:

    #all of the keys (entity) are the same, so this will number them
    if(line == "entity {\n"):
        full_text = full_text + line.replace("entity {\n", "entity" + str(i) + " {\n")
        i = i + 1
        
    else:
        full_text = full_text + line

# Replacing all of the " with nothing (we will add them back
full_text = full_text.replace('"', '')

#removing the square brackets (they are in the wrong spot)
full_text = full_text.replace('[','')
full_text = full_text.replace(']','')

# Making response s2 so it is easy to keep track of each change I made
s2 = full_text

# Surrounding any word with "
s3 = re.sub('(\w+)', '"\g<1>"', s2)

# Replacing "." with . because s3 also surrounds . with quotes
s4 = re.sub('"\."', '.', s3)

# Adding : between " { because some keys do not have a colan
s5 = re.sub('" {', '": {', s4)

# Adding curly brackets at the start and the end of the schedule and a name for it so we can loop through it
s6 = '{' + s5 + '}'

# Adding a comma after each line ending with a "
s7 = re.sub('"\n', '",\n', s6)

# Removing any extraneous white spaces
s8 = re.sub('\s', '', s7)

# Removing the commas which were added in the wrong spot
s9 = s8.replace('",}', '"}')

# Adding a coma at the end of each curly bracket that comes before a key
s10 = s9.replace('"}"', '"},"')

# Moving " to go before the - in a negative number
s11 = s10.replace(':-"', ':"-')

# Adding a comma after a curly bracket that is before a key but after another bracket
s12 = s11.replace('}"', '},"')
    
#print(s12)

#converting our reformatted string into a json file (we can read it like a bunch of nested dictioionaries)
bus_data = json.loads(s12)

#.keys loops throgh the dictionary keys and .items loops through what is in the keys
for item in bus_data.keys():

    if item.__contains__('entity'):
        print(bus_data[item]["vehicle"]["trip"]["route_id"])
        print("latitude: " + bus_data[item]["vehicle"]["position"]["latitude"])
        print("longitude: " + bus_data[item]["vehicle"]["position"]["longitude"]+"\n")
