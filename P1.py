import tkinter as tk

def run(metar_filename):
        #File handling
        fin = open(metar_filename,"r")
        choices = []
        timecodes = []
        wind = []
        windgust = []
        visL = []
        vis = []
        vis2 = []
        tempdew = []
        alt = []
        altimeter = []
        while True:
                data = fin.readline()
                if data == "":
                        break
                csv_list = data.split(' ')
                if "RMK" in csv_list:
                        rmk_i = csv_list.index("RMK")
                        del csv_list[rmk_i:]
                choices.append(csv_list[0])
                csv_list.remove(csv_list[0])
                timecodes.append([string for string in csv_list if "Z" in string])
                wind.append([string for string in csv_list if "KT" in string])
                visL.append([string for string in csv_list if "SM" in string])
                tempdew.append([string for string in csv_list if "/" in string and "SM" not in string])
                alt.append([string for string in csv_list if string.startswith("A") and len(string) == 5])

        timecodes = [s for sub in timecodes for s in sub]
        date = [string[:2] for string in timecodes]
        utc = [string[2:6] for string in timecodes]
        wind = [s for sub in wind for s in sub]
        windir = [string[:3] for string in wind]
        windspd = [string[3:5] for string in wind]
        alt = [s for sub in alt for s in sub]
        for string in wind:
                if "G" in string:
                        start = string.find("G") + 1
                        end = start + 2

                        windgust.append(string[start:end])
                else:
                        windgust.append("0")

        visL = [s for sub in visL for s in sub]
        vis = [string[:-2] for string in visL]
        for string in vis:
                if "/" in string:
                        v_index = string.index("/")
                        num = string[:-2]
                        den = string[v_index + 1:]
                        nstring =  str(int(num)/int(den))
                        vis2.append(nstring)
                else:
                        vis2.append(string)

        tempdew = [s for sub in tempdew for s in sub]
        temp = [(float(string[:-3])*9/5)+32 for string in tempdew]
        dew = [(float(string[3:])*9/5)+32 for string in tempdew]
        for string in alt:
                altimeter.append(string[1:3] + "." + string[3:5])

        #print(choices)
        #print(timecodes)
        #print(date)
        #print(utc)
        #print(wind)
        #print(windir)
        #print(windspd)
        #print(windgust)
        #print(visL)
        #print(vis)
        #print(vis2)
        #print(tempdew)
        #print(temp)
        #print(dew)
        #rrint(alt)
        #print(altimeter)


        dir = {}
        count = 0
        for a in choices:
                dir[a] = {}
                dir[a]["date"] = date[count]
                dir[a]["utc"] = utc[count]
                dir[a]["wind_dir"] = windir[count]
                dir[a]["wind_speed"] = windspd[count]
                dir[a]["wind_gust"] = windgust[count]
                dir[a]["vis"] = vis2[count]
                dir[a]["degrees"] = temp[count]
                dir[a]["dewpoint"] = dew[count]
                dir[a]["altimeter"] = altimeter[count]
                count += 1

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
        #  choices = ["KMOR", "KTYS", "KLSV", "KLAS", "KVGT", "PHNL", "KBNA"]

        # Create a variable that will store the currently selected choice.
        listvar         = tk.StringVar(root)
        time            = tk.StringVar(root)
        wind_dir        = tk.StringVar(root)
        wind_speed      = tk.StringVar(root)
        wind_gust       = tk.StringVar(root)
        vis             = tk.StringVar(root)
        degrees         = tk.StringVar(root)
        dewpoint        = tk.StringVar(root)
        altim           = tk.StringVar(root)
        # Immediately set the choice to the first element. Double check to make sure choices[0] is valid!
        listvar.set(choices[0])
        time.set(utc[0])
        wind_dir.set(windir[0])
        wind_speed.set(windspd[0])
        wind_gust.set(windgust[0])
        vis.set(vis2[0])
        degrees.set(temp[0])
        dewpoint.set(dew[0])
        altim.set(altimeter[0])
        # Create the dropdown menu with the given choices and the update variable. This is stored on the
        # list frame. You must make sure that choices is already fully populated.
        dropdown = tk.OptionMenu(list_frame, listvar, *choices)
        # The dropdown menu is on the top of the screen. This will make sure it is in the middle.
        dropdown.grid(row=0,column=1)
        # This function is called whenever the user selects another. Change this as you see fit.

        def interp(y1,y2,f,f1,f2):
                y = y1 + ((float(f)/90 * 200) - f1) * ((f2-f1)/(f2-f1))
                return y

        def drop_changed(*args):

                time.set(dir[listvar.get()]["utc"])
                wind_dir.set(dir[listvar.get()]["wind_dir"])
                wind_speed.set(dir[listvar.get()]["wind_speed"])
                wind_gust.set(dir[listvar.get()]["wind_gust"])
                vis.set(dir[listvar.get()]["vis"])
                degrees.set(dir[listvar.get()]["degrees"])
                dewpoint.set(dir[listvar.get()]["dewpoint"])
                altim.set(dir[listvar.get()]["altimeter"])


                canvas.delete("all")
                canvas.create_text(100, 100, text=listvar.get(), fill="black", tags="airport_text")
                canvas.create_oval(300, 100, 400, 200, fill="gray")
                canvas.create_oval(345, 145, 355, 155, fill="red")
                canvas.create_text(300, 205, text=str(int(wind_speed.get())) + 'MPH', fill="black", tags="airport_text")
                canvas.create_text(325, 220, text='Gust: ' + str(int(wind_gust.get())) + 'MPH', fill="black", tags="airport_text")
                canvas.create_oval(300, 250, 400, 350, fill="black")
                canvas.create_text(350, 305, text=altim.get(), fill="white", tags="airport_text")
                canvas.create_text(100, 140, text=time.get(), fill="black", tags="airport_text")
                canvas.create_rectangle(300, 400, (400/10*float(vis.get()))+300, 500, fill="orange")
                canvas.create_text(310, 520, text=str((vis.get())) + 'SM', fill="green", tags="airport_text")
                canvas.create_rectangle(300, 400, 700, 500, width=5, outline="black")

                print(400/10*float(vis.get()))
                canvas.create_rectangle(500, -(200/90*float(degrees.get())- 300), 600, 300, width=5, fill="red")
                canvas.create_text(550, 320, text=str(float(degrees.get())) + 'F', fill="red", tags="airport_text")
                canvas.create_rectangle(500, -(200/90*float(dewpoint.get())- 300), 600, 300, width=5, fill="blue")
                canvas.create_text(550, 340, text=str(float(dewpoint.get()))+'F', fill="blue", tags="airport_text")
                canvas.create_rectangle(500, 100, 600, 300, width=5, outline="black")
                print(degrees.get(),dewpoint.get())
                # Listen for the dropdown to change. When it does, the function drop_changed is called.
        listvar.trace('w', drop_changed)

        # You need to draw the text manually with the first choice.
        drop_changed()
        # mainloop() is necessary for handling events
        tk.mainloop()

# Entry point for running programs
if __name__ == "__main__":
        run(input("Enter metar file name: "))

