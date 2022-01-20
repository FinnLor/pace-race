


# import required libraries
from shapely.geometry import LineString, Point
import numpy as np
import tkinter as tk

# preferences
canvas_width = 1196
canvas_height = 664 
road_width_min = 12 
road_width_max = 26
road_width = int(np.round(0.5*(road_width_min+road_width_max)))
width_ok = False
length_ok = False
points_x = []
points_y = []
line_data = [] # prepared to generate



ui_green = '#b3ffb3'
ui_orange = '#ff8844'

global test1
test1=[]


def apply_RoadWidth():
    global width_ok
    global road_width
    try:
        road_width = int(entry_RoadWidth.get())
        if road_width >11 and road_width <26:
            label_RoadWidthCheck.configure(text ='i.O.', background=ui_green)
            width_ok = True
        else:
            label_RoadWidthCheck.configure(text ='ungültig. Vorgaben beachten.', background=ui_orange)
            width_ok = False
    except:
        label_RoadWidthCheck.configure(text ='ungültig. Vorgaben beachten.', background=ui_orange)
        width_ok = False
    set_status()


def reset_RoadPath():
    global length_ok
    global line_data
    global points_x
    global points_y
    points_x = []
    points_y = []
    line_data = []
    canvas_pace.delete('all')
    length_ok = False
    apply_RoadPath()


def extend_RoadPath(event):
    global points_x
    global points_y
    points_x = np.append(points_x, event.x)
    points_y = np.append(points_y, event.y)
    canvas_pace.create_line(event.x-5,event.y+5,event.x+5,event.y-5)
    canvas_pace.create_line(event.x-5,event.y-5,event.x+5,event.y+5)

    
def apply_RoadPath():
    global length_ok 
    global line_data
    global line_string
    try:
        line_data = np.transpose([points_x,points_y])
        if np.shape(line_data)[0]>1:
            label_RoadPathCheck.configure(text ='i.O.', background=ui_green)
            length_ok = True
        else:
            label_RoadPathCheck.configure(text ='ungültig. Vorgaben beachten.', background=ui_orange)
            length_ok = False
    except:
        label_RoadPathCheck.configure(text ='ungültig. Vorgaben beachten.', background=ui_orange) 
        length_ok = False
    set_status()


def set_status():
    if length_ok == False or width_ok == False:
        label_RoadOkCheck.configure(text = 'Daten nicht vollständig', background=ui_orange)
    else:
        label_RoadOkCheck.configure(text = 'Daten vollständig', background=ui_green)

    
def closeUI():
    ui_pace.destroy()     
    line_string = LineString(line_data)
    print(road_width)
    print(line_data)
    print(line_string)
    return road_width, line_string


def ui_about():
    print('ABOUT')
    ui_about = tk.Tk()
    ui_about.title('ABOUT')
    ui_about.geometry('400x240')
    ui_about.resizable(width=False, height=False)


# create ui_pace window
ui_pace = tk.Tk()
ui_pace.title('OKS_PaceRace_Streckeneingabemaske')
ui_pace.geometry('1200x800')
ui_pace.resizable(width=False, height=False)

# items
item_info = tk.Menu(ui_pace)
item_about = tk.Menu(item_info)
item_about.add_command(label='About', command=ui_about)
item_info.add_cascade(label='Info', menu=item_about)
ui_pace.config(menu=item_info)

# canvas
canvas_pace = tk.Canvas(ui_pace, width=canvas_width, height=canvas_height, background='white', offset='s')
canvas_pace.grid(row=3, column=0, columnspan=4)

# static text
label_RoadWidthText = tk.Label(ui_pace, text =f'STRAßENBREITE als ganze Zahl in Meter eingeben. Wertebereich in Meter [{road_width_min}-{road_width_max}]:')
label_RoadWidthText.grid(row=0, column=0, sticky = 'W')
label_RoadPath = tk.Label(ui_pace, text = 'Mindestens zwei PUNKTE als Streckenverlauf erfassen (1 Pixel entspricht 1 Meter):')
label_RoadPath.grid(row=1, column=0,sticky = 'W')
label_CloseUI = tk.Label(ui_pace, text = 'Bei gültigen Daten werden diese übernommen und die GUI geschlossen:')
label_CloseUI.grid(row=2, column=0,sticky = 'W')

# interactive text
label_RoadWidthCheck = tk.Label(ui_pace, text = 'ungültig', width=25, background=ui_orange)
label_RoadWidthCheck.grid(row=0, column=3, sticky = 'W')
label_RoadPathCheck = tk.Label(ui_pace, text = 'ungültig', width=25, background=ui_orange)
label_RoadPathCheck.grid(row=1, column=3, sticky = 'W')
label_RoadOkCheck = tk.Label(ui_pace, text = 'Daten nicht vollständig', width=25, background=ui_orange)
label_RoadOkCheck.grid(row=2, column=3, sticky = 'W')

# create entry
entry_RoadWidth = tk.Entry(ui_pace, width = 10)
entry_RoadWidth.grid(row=0, column=1)
entry_RoadWidth.insert('end', road_width)

# create buttons
button_ApplyRoadWidth = tk.Button(ui_pace, text = 'übernehmen', command = apply_RoadWidth, width = 15)
button_ApplyRoadWidth.grid(row=0, column=2)
button_ResetRoadPath= tk.Button(ui_pace, text = 'neu', command = reset_RoadPath, width = 10)
button_ResetRoadPath.grid(row=1, column=1)
button_ApplyRoadPath = tk.Button(ui_pace, text = 'übernehmen', command = apply_RoadPath, width = 15)
button_ApplyRoadPath.grid(row=1, column=2)
button_CloseUI = tk.Button(ui_pace, text = 'schließen', command = closeUI, width = 15)
button_CloseUI.grid(row=2, column=2)

# left mouseclick action
canvas_pace.bind('<Button-1>',extend_RoadPath)

# # execute tkinter
ui_pace.mainloop()






