#Tristan Wall: twall4
#COSC-505: Project A, Dictionary creatation
#This is a function that converts METAR txt files into dictionaries

#Function is setup to take a .txt file as input
def METARdict():
    #initializes dictionaries and reads METAR file
    fin = open(input("Input desired METAR file as a text file(filename.txt): "))
    innerdict = {}
    maindict = {}
    #Carries out dictionary population for each METAR line
    for line in  fin:
        parts = line.split(" ")
        airport = parts[0]
        for i in range(len(parts)):
            #parses time data into Date and UTC time
            if parts[i][-1:] == 'Z' and i > 0:
                parts[i] = parts[i][:-1]
                date = int(parts[i][:2])
                UTC = int(parts[i][2:])
                                         
            #Parses wind speed information
            elif parts[i][-2:] == 'KT' and i > 0:
                temp_wind = parts[i][:-2]
                wind_dir = int(parts[i][0:3])
                wind_speed = int(parts[i][3:5]) 
                if 'G' in temp_wind:
                    gust = int(temp_wind[-2:])
                else:
                    gust = 0
                                                    
            #Parses Visibility data
            elif parts[i][-2:] == 'SM' and i > 0 :
                temp_vis = parts[i][:-2]
                if '/' in temp_vis:
                    fract_vis = temp_vis.split('/')
                    vis = int(fract_vis[0])/int(fract_vis[1])
                else:
                    vis = int(temp_vis)

            #Parses Temperature and Dew point data 
            elif '/' in parts[i] and i >0 and not 'A' in parts[i]:
                tempOVERdew = parts[i].split('/')
                temperature = int(tempOVERdew[0])
                dewpoint =  int(tempOVERdew[1])
        
            #Parses Altitude data 
            elif parts[i][0] == 'A' and i > 0 and len(parts[i]) == 5:
                altimeter = int(parts[i][1:3]) + int(parts[i][3:])/100 
    #creates inner dictiona
        innerdict["date"] = date
        innerdict["UTC"] = UTC
        innerdict["wind_dir"] = wind_dir
        innerdict["wind_speed"] = wind_speed
        innerdict["wind_gust"] = gust
        innerdict["vis"] = vis
        innerdict["degrees"] = temperature
        innerdict["dewpoint"] = dewpoint
        innerdict["altimeter"] = altimeter
        maindict[airport] = dict(innerdict)
    return maindict


f = METARdict()
print(f)
