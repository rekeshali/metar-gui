# COSC 505: Project 1
# Group A9: rali1, twall4, hortizme, rborden4
# Display METARS data from a text file onto GUI.
import tkinter as tk

# (twall4 & hortizme) Construct dict from metars file
def METARdict(fname):
    # Initialize dictionaries
    innerdict = {}
    maindict = {}
    # Carry out dictionary population for each METAR line
    fin = open(fname, "r")
    for line in fin:
        parts = line.split(" ")
        airport = parts[0]
        for i in range(len(parts)):
            # (twall4) Parse time data into Date and UTC time
            if parts[i][-1:] == 'Z' and i > 0:
                parts[i] = parts[i][:-1]
                date = int(parts[i][:2])
                UTC = int(parts[i][2:])
            # (twall4) Parse wind speed information
            elif parts[i][-2:] == 'KT' and i > 0:
                temp_wind = parts[i][:-2]
                wind_dir = int(parts[i][0:3])
                wind_speed = int(parts[i][3:5]) 
                if 'G' in temp_wind:
                    gust = int(temp_wind[-2:])
                else:
                    gust = 0
            # (twall4) Parse Visibility data
            elif parts[i][-2:] == 'SM' and i > 0 :
                temp_vis = parts[i][:-2]
                if '/' in temp_vis:
                    fract_vis = temp_vis.split('/')
                    vis = int(fract_vis[0])/int(fract_vis[1])
                else:
                    vis = int(temp_vis)
            # (hortizme) Parse Temperature and Dew point data 
            elif '/' in parts[i] and i > 0 and not 'A' in parts[i]:
                tempOVERdew = parts[i].split('/')
                temperature = int(tempOVERdew[0])
                dewpoint =  int(tempOVERdew[1])
            # (hortizme) Parse Altitude data 
            elif parts[i][0] == 'A' and i > 0 and len(parts[i]) == 5:
                altimeter = int(parts[i][1:3]) + int(parts[i][3:])/100 
        # (hortizme) Fill inner dictionary, then main dict
        innerdict["date"] = date
        innerdict["utc"] = UTC
        innerdict["wind_dir"] = wind_dir
        innerdict["wind_speed"] = wind_speed
        innerdict["wind_gust"] = gust
        innerdict["vis"] = vis
        innerdict["degrees"] = temperature
        innerdict["dewpoint"] = dewpoint
        innerdict["altimeter"] = altimeter
        maindict[airport] = dict(innerdict)
    return maindict

def run(metar_filename):
    # Create the root Tk()
    root = tk.Tk()
    # Set the title to your group's name Project A 1, 2, 3, etc.
    root.title("COSC505 - Project A 9")
    # Create two frames, the list is on top of the Canvas
    list_frame = tk.Frame(root)
    draw_frame = tk.Frame(root)
    # Set the list grid in c,r = 0,0
    list_frame.grid(column=0, row=0)
    # Set the draw grid in c,r = 0,1
    draw_frame.grid(column=0,row=1)

    # Create the canvas on the draw frame, set the width to 800 and height to 600
    canvas = tk.Canvas(draw_frame, width=800, height=600)
    # Reset the size of the grid
    canvas.pack()

    # THESE ARE EXAMPLES! You need to populate this list with the available airports in the METAR file
    # which is given by metar_file passed into this function.
    data_all = METARdict(metar_filename)
    choices = list(data_all.keys())

    # Create a variable that will store the currently selected choice.
    listvar = tk.StringVar(root)
    # Immediately set the choice to the first element. Double check to make sure choices[0] is valid!
    listvar.set(choices[0])

    # Create the dropdown menu with the given choices and the update variable. This is stored on the
    # list frame. You must make sure that choices is already fully populated.
    dropdown = tk.OptionMenu(list_frame, listvar, *choices)
    # The dropdown menu is on the top of the screen. This will make sure it is in the middle.
    dropdown.grid(row=0,column=1)

    ###############################################################################################
    # (rborden4 & rali1) Routines for drawing all the necessary objects on the display
    # (rborden4) Airport name
    def draw_name(name):
        x, y = 100, 100
        canvas.create_text(x, y, text=name, font=('Courier', 32), fill="red", anchor='nw')
        return
    # (rborden4) Date (actually just time)
    def draw_date(time):
        x, y = 100, 100
        half_time = time - 1200*(time>=1300) + 1200*(time<100)
        text_time = str(half_time) + "am"*(time<1200) + "pm"*(time>=1200)
        canvas.create_text(x, y+32, text=text_time, font=('Courier', 32), fill="blue", anchor='nw')
        return
    # (rborden4) Wind gauge
    def draw_wind(speed, gust, angle):
        # Sizing variables
        x, y = 300, 100
        w, h = 100, 100
        # Big circle
        canvas.create_oval(x, y, x+w, y+h, fill="darkgray")
        # Display speed
        if(speed): # If nonzero
            speed      = round(speed*1.15)
            text_speed = str(speed) + "MPH"
            canvas.create_text(x, y+h+6, text=text_speed, font=("Courier", 14), fill="black", anchor="w")
        else: # Otherwise print calm
            canvas.create_text(x, y+h+6, text="CALM", font=("Courier", 14), fill="black", anchor="w")
        # Display gust 
        if(gust):
            gust = round(gust*1.15)
            text_gust  = "Gust: " + str(gust) + "MPH"
            canvas.create_text(x, y+h+18, text=text_gust, font=("Courier", 14), fill="black", anchor="w")
        # Display angle
        if(angle):
            canvas.create_arc(x, y, x+w, y+h, start=angle+90-1, extent=3, fill="white")
        # Small circle
        tiny = 20
        canvas.create_oval(x+w/2-w/tiny, y+h/2-h/tiny, x+w/2+w/tiny, y+h/2+h/tiny, fill="red")
        return
    # (rali1) Temperature gauge
    def draw_temp(temp, dewp):
        # Sizing variables
        x, y = 500, 100
        w, h = 100, 200
        # Converting from C to F
        temp = 1.8*temp + 32
        dewp = 1.8*dewp + 32
        # Display gauge
        maxt = 90 # max temp in F
        canvas.create_rectangle(x, y, x+w, y+h, width=4) # Base rectangle
        canvas.create_rectangle(x, y+h*(1-temp/maxt), x+w, y+h, width=4, fill="red")
        canvas.create_rectangle(x, y+h*(1-dewp/maxt), x+w, y+h, width=4, fill="blue")
        # Display text
        text_temp = "%.1fF" % temp
        text_dewp = "%.1fF" % dewp
        canvas.create_text(x+w/2, y+h+18,   text=text_temp, font=("Courier", 18), fill="red")
        canvas.create_text(x+w/2, y+h+2*18, text=text_dewp, font=("Courier", 18), fill="blue")
        return
    # (rali1) Altimeter
    def draw_alt(alt):
        # Sizing variables
        x, y = 300, 250
        w, h = 100, 100
        # Black circle w/text
        text_alt = "%.2f" % alt
        canvas.create_oval(x, y, x+w, y+h, fill="black")
        canvas.create_text(x+w/2, y+h/2, text=text_alt, font=("Courier", 18), fill="white")
        return
    # (rali1) Visibility gauge
    def draw_vis(vis):
        # Sizing variables
        x, y = 300, 400
        w, h = 400, 100
        # Display gauge
        maxv = 10 # max vis
        canvas.create_rectangle(x, y, x+w, y+h, width=5) # Base rectangle
        canvas.create_rectangle(x, y, x+w*vis/maxv, y+h, width=5, fill="orange")
        # Display text
        text_vis = str(vis) + "SM"
        canvas.create_text(x, y+h+14,   text=text_vis, font=("Courier", 14), fill="darkgreen", anchor="w")
        return
    ###############################################################################################

    # (rali1 & rborden4) This function is called whenever the user selects another. Change this as you see fit.
    def drop_changed(*args):
        # Clear contents
        canvas.delete("all")
        # Get name of selection
        name_port = listvar.get() # name of selected airport
        data_port = data_all[name_port] # data from selected airport
        # Update display
        draw_name(name_port)
        draw_date(data_port['utc'])
        draw_wind(data_port['wind_speed'], data_port['wind_gust'], data_port['wind_dir'])
        draw_temp(data_port['degrees'], data_port['dewpoint'])
        draw_alt (data_port['altimeter'])
        draw_vis (data_port['vis'])

    # Listen for the dropdown to change. When it does, the function drop_changed is called.
    listvar.trace('w', drop_changed)
    # You need to draw the text manually with the first choice.
    drop_changed()
    # mainloop() is necessary for handling events
    tk.mainloop()

# Entry point for running programs
if __name__ == "__main__":
        run(input("Enter metar file name: "))
