import tkinter as tk

def run(metar_filename):
        # Create the root Tk()
        root = tk.Tk()
        # Set the title to your group's name Project A 1, 2, 3, etc.
        root.title("COSC505 - Project A")
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
        choices = ["KONE", "KTWO", "KTHRE"]

        # Create a variable that will store the currently selected choice.
        listvar = tk.StringVar(root)
        # Immediately set the choice to the first element. Double check to make sure choices[0] is valid!
        listvar.set(choices[0])

        # Create the dropdown menu with the given choices and the update variable. This is stored on the
        # list frame. You must make sure that choices is already fully populated.
        dropdown = tk.OptionMenu(list_frame, listvar, *choices)
        # The dropdown menu is on the top of the screen. This will make sure it is in the middle.
        dropdown.grid(row=0,column=1)

        ######

        # Temp gauge (rborden4)
        def temp_gauge(temperature, dewpoint):
            # starting coordinates
            x, y = 500, 100
            # size
            w, h = 100, 200
            # convert temp and dewpoint to Fahrenheit
            tempf = 1.8 * temperature + 32
            dewf = 1.8 * dewpoint + 32
            # text for temp gauge
            temp_text = "%.1fF" % tempf
            dew_text = "%.1fF" % dewf
            # temperature range 0-90
            maxt = 90
            # draw rectangles
            canvas.create_rectangle(x, y, (x + w), (y + h))
            canvas.create_rectangle(x, (y + h) * (1 - temperature / maxt), (x + w), (y + h), (fill = "red"))
            canvas.create_rectangle(x, (y + h) * (1 - dewpoint / maxt), (x + w), (y + h), (fill = "blue"))
            # display text on gauge
            canvas.create_text((x + w / 2), (y + h + 18), text = temp_text, font = ("Courier", 18), (fill = "red"))
            canvas.create_text((x + w / 2), (y + h + 2 * 18), text = dew_text, font = ("Courier", 18), (fill = "blue"))

        # Altimeter gauge (rborden4)
        def alt_gauge(altimeter):
            # starting coordinates
            x, y = 300, 250
            # size
            w, h = 100, 100
            # text for altimeter gauge
            alt_text = 
            # draw oval
            canvas.create_oval(x, y, (x + w), (y + h), (fill = "black"))
            # add text
            canvas.create_text((x + w / 2), (y + h / 2), text = alt_text, font = ("Courier", 18), (fill = "white"))
             
        # Visibility gauge (rborden4)
        def vis_gauge(vis):
            # starting coordinates
            x, y = 300, 400
            # size
            w, h = 400, 100
            # visibility range 0-10
            vis_max = 10
            # draw rectangles
            canvas.create_rectangle(x, y, (x + w), (y + h))
            canvas.create_rectangle(x, y, (x + w * vis / vis_max), (y + h), (fill = "orange"))
            # draw text
            vis_text = str(vis) + "SM"
            canvas.create_text(x, (y + h + 14), text = vis_text, font=("Courier", 14), fill = "darkgreen", anchor = "w")
            
        ######

        
        # This function is called whenever the user selects another. Change this as you see fit.
        def drop_changed(*args):
                canvas.delete("airport_text")
                canvas.create_text(100, 100, text=listvar.get(), fill="black", tags="airport_text")
        # Listen for the dropdown to change. When it does, the function drop_changed is called.
        listvar.trace('w', drop_changed)
        # You need to draw the text manually with the first choice.
        drop_changed()
        # mainloop() is necessary for handling events
        tk.mainloop()

# Entry point for running programs
if __name__ == "__main__":
        run(input("Enter metar file name: "))
