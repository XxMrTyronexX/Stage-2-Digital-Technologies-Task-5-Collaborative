import requests
import json
import os
import re
import linecache
import io

#putting URL containing bus data inside of requests object
r1 = requests.get("https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions/debug")
r2 = requests.get("https://gtfs.adelaidemetro.com.au/v1/realtime/service_alerts/debug")

#extracting the bus timetable data from the object as a string
response1 = r1.text
response2 = r2.text

#getting the lines of the string returned
lines_of_response1 = io.StringIO(response1).readlines()
lines_of_response2 = io.StringIO(response2).readlines()

#creating blank variables to be concatinated or iterated on
full_text1 = ""
full_text2 = ""
i = 1
j = 1
k = 1

#looping through each line of the bus schedule
for line in lines_of_response1:

    #all of the keys (entity) are the same, so this will number them
    if(line == "entity {\n"):
        full_text1 = full_text1 + line.replace("entity {\n", "entity" + str(i) + " {\n")
        i = i + 1
        
    else:
        full_text1 = full_text1 + line

#looping through each line of the service alerts
for line in lines_of_response2:

    if(line == "    informed_entity {\n"):
        full_text2 = full_text2 + line.replace('    informed_entity {\n', '    "informed_entity' + str(j) + '": {\n')
        j = j + 1
        
    elif(line == "entity {\n"):
        full_text2 = full_text2 + line.replace('entity {\n', '"entity' + str(k) + '": {\n')
        k = k + 1
        
    else:
        full_text2 = full_text2 + line

# Replacing all of the " with nothing (we will add them back
full_text1 = full_text1.replace('"', '')\

#removing the square brackets (they are in the wrong spot)
full_text1 = full_text1.replace('[','')
full_text1 = full_text1.replace(']','')
full_text2 = full_text2.replace('[','')
full_text2 = full_text2.replace(']','')

# Making response s2 so it is easy to keep track of each change I made
vehicle_positions2 = full_text1
service_alerts2 = "{" + full_text2 + "}"

# Surrounding any word with "
vehicle_positions3 = re.sub('(\w+)', '"\g<1>"', vehicle_positions2)\

# Replacing "." with . because s3 also surrounds . with quotes
vehicle_positions4 = re.sub('"\."', '.', vehicle_positions3)

# Adding : between " { because some keys do not have a colan
vehicle_positions5 = re.sub('" {', '": {', vehicle_positions4)

# Adding curly brackets at the start and the end of the schedule and a name for it so we can loop through it
vehicle_positions6 = '{' + vehicle_positions5 + '}'

# Adding a comma after each line ending with a "
vehicle_positions7 = re.sub('"\n', '",\n', vehicle_positions6)

# Removing any extraneous white spaces
vehicle_positions8 = re.sub('\s', '', vehicle_positions7)

# Removing the commas which were added in the wrong spot
vehicle_positions9 = vehicle_positions8.replace('",}', '"}')

# Adding a coma at the end of each curly bracket that comes before a key
vehicle_positions10 = vehicle_positions9.replace('"}"', '"},"')

# Moving " to go before the - in a negative number
vehicle_positions11 = vehicle_positions10.replace(':-"', ':"-')

# Adding a comma after a curly bracket that is before a key but after another bracket
vehicle_positions12 = vehicle_positions11.replace('}"', '},"')

#formatting the service alerts return value so it can be read in json format
service_alerts3 = re.sub('header {', '"header": {', service_alerts2)
service_alerts4 = re.sub('      route_id: ', '      "route_id": ', service_alerts3)
service_alerts5 = re.sub('  gtfs_realtime_version: ', '  "gtfs_realtime_version": ', service_alerts4)
service_alerts6 = re.sub('  incrementality: ', '  "incrementality": "', service_alerts5)
service_alerts7 = re.sub('  id: ', '  "id": ', service_alerts6)
service_alerts8 = re.sub('  timestamp: ', '  "timestamp": "', service_alerts7)
service_alerts9 = re.sub('    active_period {', '    "active_period": {', service_alerts8)
service_alerts10 = re.sub('  alert {', '  "alert": {', service_alerts9)
service_alerts11 = re.sub('      start: ', '      "start": "', service_alerts10)
service_alerts12 = re.sub('    cause: ', '    "cause": "', service_alerts11)
service_alerts13 = re.sub('    effect: ', '    "effect": "', service_alerts12)
service_alerts14 = re.sub('    url {', '    "url": {', service_alerts13)
service_alerts15 = re.sub('      translation {', '       "translation": {', service_alerts14)
service_alerts16 = re.sub('        text: ', '        "text": ', service_alerts15)
service_alerts17 = re.sub('    header_text {', '    "header_text": {', service_alerts16)
service_alerts18 = re.sub('        language: ', '        "language": ', service_alerts17)
service_alerts19 = re.sub('    description_text {', '    "description_text": {', service_alerts18)

service_alerts20 = re.sub('\n.*?}"', '"\n"' , service_alerts19, flags=re.DOTALL)
service_alerts21 = re.sub('\n', '",\n' , service_alerts20)
service_alerts22 = re.sub(' {",', ' {' , service_alerts21)
service_alerts23 = re.sub('"",\n','",\n' , service_alerts22)
service_alerts24 = service_alerts23.replace(': {",\n', ': {\n')
service_alerts25 = service_alerts24.replace('",\n}",', '"\n},')
service_alerts26 = service_alerts25.replace('",\n }",', '"\n },')
service_alerts27 = service_alerts26.replace('",\n  }",', '"\n  },')
service_alerts28 = service_alerts27.replace('",\n   }",', '"\n   },')
service_alerts29 = service_alerts28.replace('",\n    }",', '"\n    },')
service_alerts30 = service_alerts29.replace('",\n     }",', '"\n    },')
service_alerts31 = service_alerts30.replace(',\n      }"', '\n      }')
service_alerts32 = service_alerts31.replace('      }\n    },\n  }"', '      }\n    }\n  }')
service_alerts33 = re.sub('\<.*?>', '' , service_alerts32, flags=re.DOTALL)
service_alerts34 = re.sub('      end: ', '      "end": "', service_alerts33)
service_alerts35 = re.sub('},\n}', '}\n}', service_alerts34)

#converting our reformatted string into a json file (we can read it like a bunch of nested dictioionaries)
bus_position_data = json.loads(vehicle_positions12)
service_alert_data = json.loads(service_alerts35)

#.keys loops throgh the dictionary keys and .items loops through what is in the keys

#function to get all of the latitude and longitude coordinates of the busses with the number the user enters as a series of tuples inside of a list
def get_bus_location(bus_name: str) -> list[tuple]:

    #list to store the the bus coordinates as
    list_of_busses = []
    
    #loops through all of the entities
    for item in bus_position_data.keys():
        
        #if the key is for an entitiy (entities are bus entries)
        if item.__contains__('entity'):

            #if the currently selected bus matches the route number that the user has entered
            if bus_position_data[item]["vehicle"]["trip"]["route_id"] == bus_name:
                
                #add the coordinates to a tuple as a float
                temporary_tuple = (bus_position_data[item]["id"], float(bus_position_data[item]["vehicle"]["position"]["latitude"]), float(bus_position_data[item]["vehicle"]["position"]["longitude"]))

                #add the tuple to the list 
                list_of_busses.append(temporary_tuple)

    return list_of_busses


#uses the bus ID to determine if it has wheelchair acceess
def wheelchair_access (bus_id: str) -> bool:

    for item in bus_position_data.keys():

        if item.__contains__('entity'):

            if bus_position_data[item]["id"] == bus_id:

                if bus_position_data[item]["vehicle"]["vehicle"]["transit_realtime.tfnsw_vehicle_descriptor"]["wheelchair_accessible"] == "1":
                    return True

                elif bus_position_data[item]["vehicle"]["vehicle"]["transit_realtime.tfnsw_vehicle_descriptor"]["wheelchair_accessible"] == "0":
                    return False
                

#uses the bus ID to determine if it has air conditioning
def air_conditioned (bus_id: str) -> bool:

    for item in bus_position_data.keys():
        
        if item.__contains__('entity'):
            
            if bus_position_data[item]["id"] == bus_id:
                
                if bus_position_data[item]["vehicle"]["vehicle"]["transit_realtime.tfnsw_vehicle_descriptor"]["air_conditioned"] == "true":
                    return True

                elif bus_position_data[item]["vehicle"]["vehicle"]["transit_realtime.tfnsw_vehicle_descriptor"]["air_conditioned"] == "false":
                    return False


#uses the bus ID to check the bus speed
def bus_speed (bus_id: str) -> float:

    #loops through all of the entities
    for item in bus_position_data.keys():

        if item.__contains__('entity'):

            if bus_position_data[item]["id"] == bus_id:

                return float(bus_position_data[item]["vehicle"]["position"]["speed"])

                    
    

while True:
    user_input = input("Type the bus that you would like the coordinates of: ")

    print(get_bus_location(user_input))

    user_input2 = input("Again?")

    if user_input2 == "n":
        break

'''
for item in bus_position_data.keys():

    if item.__contains__('entity'):
        print(bus_position_data[item]["vehicle"]["trip"]["route_id"])
        print("latitude: " + bus_position_data[item]["vehicle"]["position"]["latitude"])
        print("longitude: " + bus_position_data[item]["vehicle"]["position"]["longitude"]+"\n")
'''
