
import PySimpleGUI as sg
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random 
from PIL import Image, ImageTk

"""
UI Functions:
    draw_figure - Draws UI plot
    time_as_int - Updates UI runtime
"""
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def time_as_int():
    return int(round(time.time() * 100))

def make_table(num_cols, num_rows):
    data = [['' for row in range(num_cols)] for col in range(num_rows)]
    data[0][0] = 'Sensor Source'
    data[1][0] = 'Left Battery Charge (percentage)'
    data[2][0] = 'Right Battery Charge (percentage)'
    data[3][0] = 'Latitude (decimal)'
    data[4][0] = 'Longitude (decimal)'
    data[5][0] = 'Heading (degrees)'
    data[0][1] = 'Magnitude'
    data[1][1] = 0
    data[2][1] = 0
    data[3][1] = 0
    data[4][1] = 0
    data[5][1] = 0
    return data

#----------------------------------------------------------------------------------------------------------------------#
"""
Initializes UI elements, then generates UI window
"""
sg.change_look_and_feel('lightblue')
data = make_table(num_cols=2, num_rows=6)
sg.set_options(element_padding=(0,0))
headings = [data[0][x] for x in range(len(data[0]))]

# Column layout
col = [
       [sg.Frame('Output Window',[[sg.Table(values=data[1:][:], headings=headings, max_col_width=25, background_color='grey',
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left',
                num_rows=7,
                alternating_row_color='white',
                key='-TABLE-',
                tooltip='Sensor Output Table')]])],
       [sg.Frame('Console',[[sg.Output(size=(60,20))]])]
       ]
menu_def = [['&File', ['&Open', '&Save', '---', 'Properties', 'E&xit'  ]],
            ['&Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
            ['&Help', '&About...'],]
layout = [
          [sg.Menu(menu_def,)],
          [sg.Text(' ' * 45),sg.Text('BAY STATION INTERFACE - GM SURF', size=(40, 1), justification='center', font='Helvetica 20')],
          [sg.Text('_' * 165)],
          [sg.Frame('GPS Tracking',[[sg.Canvas(size=(640, 480), key='-CANVAS-')]]),
           sg.Column(col, background_color='white')],
          [sg.Text('_' * 165)],
          [sg.Text('', size=(8,2),font=('Helvetica', 20),justification='center',key='-STATUS-'),
           sg.Text(' ' * 5),
           sg.Text('', size=(8,2),font=('Helvetica', 20),justification='center',key='-TEXT-'),
           sg.Text(' ' * 5),
           sg.Frame('Ping Location',[[sg.Text('Latitude',font=('Helvetica', 20),justification='center',size=(8,2)),
           sg.In(size=(8,1),font=('Helvetica', 20),justification='center',key='-LAT-'),
           sg.Text(' ' * 5),
           sg.Text('Longitude',font=('Helvetica', 20),justification='center',size=(8,2)),
           sg.In(size=(8,1),font=('Helvetica', 20),justification='center',key='-LONG-'),
           sg.Text(' ' * 10),
           sg.Button('GO HERE',bind_return_key=True)]]),

           sg.Text(' ' * 10)],
            #sg.Image(filename=r'C:\Users\BrianAguilar\Documents\TEST_SENIOR_DESIGN\Capture.png')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
           sg.Exit(button_color=('white', 'firebrick4'), key='Exit')],
          ]
window = sg.Window('Bay Station Control', layout,
                   return_keyboard_events=True,
                   use_default_focus=False,
                   no_titlebar=True,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   finalize=True)
#----------------------------------------------------------------------------------------------------------------------#
"""
Pre Config, RASP Pi, XBee
"""
#TODO: Replace with the serial port where your local module is connected to.
#PORT = "COM4"
#TODO: Replace with the baud rate of your local module.
# BAUD_RATE = 9600
TIMEOUT = 10
#device = XBeeDevice(PORT, BAUD_RATE)
#device.open()
#message = 'GMU'

#device.set_sync_ops_timeout(TIMEOUT)
#sa = device.add_data_received_callback(data_receive_callback)
leftESC = 0
rightESC = 0

baseMessage = 'Command,Thruster,'
INCREMENT = 10

print(" +---------------------------------------------------------------------------------+")
print(" |      GMU SURF: USV BAY STATION CONTROLLER	     |")
print(" +---------------------------------------------------------------------------------+\n")
"""
Initial values to be read by UI
"""
#  timer
current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

#  plot
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas
fig, ax = plt.subplots()
ax.grid(True)
fig_agg = draw_figure(canvas, fig)
x = []
y = []
#testy = 38
#testx = -77

#  Initialize Database Class for SQLite Data Logging
#USV = Database('Indoor_Test','12-15-19',1)
eventType = 'Invalid'
check = 0
update_track = 0
test = 0

#  BMS readings
#battery_voltage = 14.8
while 1:
    # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=TIMEOUT)
        current_time = time_as_int() - start_time
        if update_track == 1:
            ax.cla()
            ax.grid(True)
            for color in ['red']:
                #x.append(testx) #GPS.latitude
                #y.append(testy) #GPS.longitude
                ax.scatter(x,y,c=color,label=color,alpha=0.3,edgecolors='none')
            ax.legend()
            fig_agg.draw()
            #USV.log('GPS',[float(testx), float(testy), float(testx)])
            update_track = 0
    else:
        event, values = window.read()
    # --------- Do Button Operations --------
    if event in (None, 'Exit'):        # ALWAYS give a way out of program
        leftESC=0
        rightESC=0
        break
    eventType = 'ESC'
    if event == '-RESET-':
        x = []
        y = []
        paused_time = start_time = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
        # Change button's text
        
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    # elif event == 'Up:38':
    #     leftESC = modifyESC(leftESC, INCREMENT)
    #     rightESC = modifyESC(rightESC, INCREMENT)
    #     print(f'L:{leftESC}, R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'Down:40':
    #     leftESC = modifyESC(leftESC, -INCREMENT)
    #     rightESC = modifyESC(rightESC, -INCREMENT)
    #     print(f'L:{leftESC}, R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'Left:37':
    #     leftESC = modifyESC(leftESC, -INCREMENT)
    #     rightESC = modifyESC(rightESC, INCREMENT)
    #     print(f'"L:{leftESC}, R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'Right:39':
    #     leftESC = modifyESC(leftESC, INCREMENT)
    #     rightESC = modifyESC(rightESC, -INCREMENT)
    #     print(f'L:{leftESC}, R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == '-STOP-':
    #     leftESC = modifyESC(0,0)
    #     rightESC = modifyESC(0,0)
    #     print(f'L:{leftESC}, R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'w':
    #     print('w: left thruster increase')
    #     leftESC = modifyESC(leftESC, INCREMENT)
    #     print(f'L:{leftESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 's':
    #     print('s: right thruster increase')
    #     leftESC = modifyESC(leftESC, -INCREMENT)
    #     print(f'L:{leftESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'r':
    #     print('r: right thruster increase')
    #     rightESC = modifyESC(rightESC, INCREMENT)
    #     print(f'R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'f':
    #     print('f: right thruster decrease')
    #     rightESC = modifyESC(rightESC, -INCREMENT)
    #     print(f'R:{rightESC}')
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)
    #     check = 1
    # elif event == 'i':
    #     eventType = 'IMU'
    #     msg = 'Command,Request,IMU'
    #     check = 1
    # elif event == 'g':
    #     eventType = 'GPS'
    #     msg = 'Command,Request,GPS'
    #     check = 1
    # elif event =='b':
    #     eventType = 'BMS'
    #     msg = 'Command,Request,BMS'
    #     check = 1
    # elif event == 'o':
    #     eventType = 'PIDON'
    #     msg = 'Command,PID,True'
    #     check = 1
    # elif event == 'p':
    #     eventType = 'PIDOFF'
    #     msg = 'Command,PID,False'
    #     check = 1
    # elif event == 'l':
    #     eventType = 'UPDATEPIDSTART'
    #     msg = 'Command,UpdatePIDStart'
    #     check = 1
    # elif event == 'c':
    #     eventType = 'TOGGLECALIBRATION'
    #     msg = 'Command,ToggleCalibration'
    #     check = 1
    # elif event == 'h':
    #     eventType = 'SAVEHEADING'
    #     msg = 'Command,SaveHeading'
    #     check = 1
    # elif event =='m':
    #     #testing
    #     x.append(100)
    #     y.append(100)
    #     x.append(random.randint(1,10))
    #     y.append(random.randint(1,10))
    #     data[2][1] = random.randint(1,10)
    #     data[3][1] = random.randint(1,10)
    #     data[4][1] = random.randint(1,10)
    #     #print(data)
    # else:
    #     msg = baseMessage + str(leftESC) + ',' + str(rightESC)

    # --------- Display timer in window --------
    window['-TEXT-'].update('Run Time {:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))
    #window['-BATTERYLVL-'].update('Battery {0:.2f}'.format(battery_voltage))
    window['-STATUS-'].update('Status\nGood')

    window['-TABLE-'].update(values=data[1:])

window.close()
