def data_fake():
    return {
'KMOR': {'date': 31, 'utc': 1435, 'wind_dir': 270, 'wind_speed': 7, 'wind_gust': 14, 'vis': 10, 'degrees': 23, 'dewpoint': 17, 'altimeter': 29.95},
'KTYS': {'date': 31, 'utc': 1353, 'wind_dir': 280, 'wind_speed': 9, 'wind_gust': 0, 'vis': 10, 'degrees': 23, 'dewpoint': 17, 'altimeter': 29.95},
'KLSV': {'date': 31, 'utc': 1355, 'wind_dir': 290, 'wind_speed': 2, 'wind_gust': 0, 'vis': 10, 'degrees': 21, 'dewpoint': 7, 'altimeter': 29.92},
'KLAS': {'date': 31, 'utc': 1356, 'wind_dir': 10, 'wind_speed': 6, 'wind_gust': 0, 'vis': 4, 'degrees': 22, 'dewpoint': 8, 'altimeter': 29.9},
'KVGT': {'date': 31, 'utc': 1353, 'wind_dir': 220, 'wind_speed': 3, 'wind_gust': 0, 'vis': 1, 'degrees': 21, 'dewpoint': 8, 'altimeter': 29.91},
'PHNL': {'date': 31, 'utc': 153, 'wind_dir': 70, 'wind_speed': 7, 'wind_gust': 0, 'vis': 3, 'degrees': 26, 'dewpoint': 19, 'altimeter': 30.01},
'KBNA': {'date': 31, 'utc': 2353, 'wind_dir': 0, 'wind_speed': 0, 'wind_gust': 0, 'vis': 0.5, 'degrees': 8, 'dewpoint': 1, 'altimeter': 29.97}
}

import tkinter as tk

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
    data_all = data_fake()
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
    # Routines for drawing all the necessary objects on the display
    # (rali1) Airport name
    def draw_name(name):
        x, y = 100, 100
        canvas.create_text(x, y, text=name, font=('Courier', 32), fill="red", anchor='nw')
        return
    # (rali1) Date (actually just time)
    def draw_date(time):
        x, y = 100, 100
        half_time = time - 1200*(time>=1300) + 1200*(time<100)
        text_time = str(half_time) + "am"*(time<1200) + "pm"*(time>=1200)
        canvas.create_text(x, y+32, text=text_time, font=('Courier', 32), fill="blue", anchor='nw')
        return
    # (rali1) Wind gauge
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
        canvas.create_rectangle(x, y, x+w, y+h, width=5) # Base rectangle
        canvas.create_rectangle(x, y+h*(1-temp/maxt), x+w, y+h, width=5, fill="red")
        canvas.create_rectangle(x, y+h*(1-dewp/maxt), x+w, y+h, width=5, fill="blue")
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

    # (rali1) This function is called whenever the user selects another. Change this as you see fit.
    def drop_changed(*args):
        # Clear contents
        canvas.delete("all")
        # Get name of selection
        name_port = listvar.get() # name of selected airport
        data_port = data_all[name_port] # data from selected airport
        # Begin updating the display
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

