import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# VARS CONSTS:
_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False,
         }
# Sample of different machines.
data = {
    'Machine1: 280v/60Hz/4-Poles': {
        'Vs': 280,
        'fr': 60,
        'p1': 4,
        'r1': 0.12,
        'r2': 0.1,
        'l1': 0.000663145,
        'l2': 0.000663145,
    },
    'Machine2: 254.034v/50Hz/8-Poles': {
        'Vs': 254.034,
        'fr': 50,
        'p1': 8,
        'r1': 0.085,
        'r2': 0.067,
        'l1': 0.000623887,
        'l2': 0.000512478,
    },
    'Machine3: 120.089v/60Hz/6-Poles': {
        'Vs': 120.089,
        'fr': 60,
        'p1': 6,
        'r1': 0.105,
        'r2': 0.0712,
        'l1': 0.00069869,
        'l2': 0.00069869,

    },
    'Machine4: 3464.102/50Hz/8-Poles': {
        'Vs': 3464.102,
        'fr': 50,
        'p1': 8,
        'r1': 1.1,
        'r2': 0.978,
        'l1': 0.0260441189,
        'l2': 0.0260441189,
    },
    'Machine5: 265.581v/60Hz/8-Poles': {
        'Vs': 265.581,
        'fr': 60,
        'p1': 8,
        'r1': 0.015,
        'r2': 0.035,
        'l1': 0.000385,
        'l2': 0.000385,
    },
    'Machine6: 400v/50Hz/8-Poles': {
        'Vs': 400,
        'fr': 50,
        'p1': 8,
        'r1': 1.1797,
        'r2': 0.7703,
        'l1': 0.005375456,
        'l2': 0.005375456,
    },
    'Machine7: 254.034v/60Hz/6-Poles': {
        'Vs': 254.034,
        'fr': 60,
        'p1': 6,
        'r1': 0.05,
        'r2': 0.064,
        'l1': 0.000616725,
        'l2': 0.000616725,
    }
}

# Theme for pyplot
plt.style.use('seaborn')
AppFont = ('Any 16', 12)
sg.theme('Default1')


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def empty_plot():
    _VARS['pltFig'] = plt.figure()
    plt.plot()
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


# Adding elements of the GUI (Textbox, Checkbox, Radio Buttons, Listbox, Labels and Buttons)
col1 = [
        [sg.Text('Use Sample Machine Rating?:', size=(23, 1)), sg.Checkbox('Enabled', key='mcEnabled', enable_events=True)],
        [sg.Text('Neglect Stator Resistance:', size=(23, 1)), sg.Checkbox('Enabled', key='clearRes', enable_events=True)]
       ]
col2 = [
        [sg.Listbox(list(data.keys()), size=(30, 4), enable_events=True, key='_LIST_')]
       ]
elements_layout = [
                [sg.Radio("Variable Freq", "RADIO", key='-CASE1-', font=("any16", 14), background_color='#C1CDCD'),
                 sg.Radio("Pole Changing", "RADIO", key='-CASE2-', font=("any16", 14), background_color='#C1CDCD'),
                 sg.Radio("V/f Operation", "RADIO", key='-CASE3-', font=("any16", 14), background_color='#C1CDCD')],
                [sg.Text("Rated Voltage (Volts):", justification='left',size=(20, 1)),
                 sg.Input(key='vs', do_not_clear=True, size=(10, 1), justification="left"),
                 sg.Text("Rated Frequency (Hz):", size=(20, 1)), sg.Input(key='fr', do_not_clear=True, size=(10, 1))],
                [sg.Text("No. of Pair Poles (1):", size=(20, 1)), sg.Input(key='p1', do_not_clear=True, size=(10, 1)),
                 sg.Text("No. of Pair Poles (2):", size=(20, 1)), sg.Input(key='p2', do_not_clear=True, size=(10, 1))],
                [sg.Text("Stator Resistance (Ohms):", size=(20, 1)), sg.Input(key='r1', do_not_clear=True, size=(10, 1)),
                 sg.Text("Rotor Resistance (Ohms):", size=(20, 1)), sg.Input(key='r2', do_not_clear=True, size=(10, 1))],
                [sg.Text("Stator Inductance (Henry):",size=(20, 1)), sg.Input(key='l1', do_not_clear=True, size=(10, 1)),
                 sg.Text("Rotor Inductance (Henry):", size=(20, 1)), sg.Input(key='l2', do_not_clear=True, size=(10, 1))],
                [sg.Column(col1, element_justification='c' ), sg.Column(col2, element_justification='c')],
                [sg.Text("Rating:", key='-lbl1-', font=("any16", 14))],
                [sg.Text("", key='-lbl2-', font=("any16", 12))],
                [sg.Canvas(key='figCanvas', background_color='#C1CDCD', expand_x=True, expand_y=True)],
                [sg.Button('Draw', font=("any16", 14), size=(10, 1)),
                 sg.Button('Exit', font=("any16", 14), size=(10, 1))]
                ]


tab_group = [
    [sg.TabGroup(
        [[sg.Tab('Graphing of Torque-Speed Characteristic', elements_layout,
                 element_justification='center')]])]
]

_VARS['window'] = sg.Window('T-n Plotter',
                            tab_group,
                            finalize=True,
                            resizable=False,
                            location=(600, 0),
                            element_justification="center",
                            font=('Any 16', 12),
                            background_color='#C1CDCD',
                            )

def drawChart():
    """
    Calculates torque using given parameters and then returns a plot of Torque-Speed Characteristic

    Parameters:
    Vs     -- Rated Voltage (float)
    fr     -- Rated Frequency (int)
    p1, p2 -- Number of pair poles (int)
    r1, r2 -- Stator, Rotor Resistance (float)
    l1, l2 -- Stator, Rotor Inductance (float)
    """
    _VARS['fig_agg'].get_tk_widget().forget()
    s = np.arange(0.0001, 1.001, 0.001)

    # To get values from list of samples if the first checkbox is enabled,
    # This gets the value of the parameters of selected machine from listbox
    # and then converts it into a list.
    if values['mcEnabled']:
        selectedMach = list(data.get(values['_LIST_'][0]).values())
        Vs = selectedMach[0]
        fr = selectedMach[1]
        p1 = selectedMach[2]
        r1 = selectedMach[3]
        r2 = selectedMach[4]
        l1 = selectedMach[5]
        l2 = selectedMach[6]
    else:                               # To get values from the user through a specified textbox
        Vs = float(values['vs'])
        fr = int(values['fr'])
        p1 = int(values['p1'])
        r1 = float(values['r1'])
        r2 = float(values['r2'])
        l1 = float(values['l1'])
        l2 = float(values['l2'])
    if values['clearRes']:              # Clear stator resistance if the second checkbox is enabled
        r1 = 0
    if p1 % 2 != 0:
        raise Exception
    # Rating labels:
    _VARS['window']['-lbl1-'].update("Rating: {} volts, {} Hz, {} RPM, {}-Poles,".format(Vs, fr, 60*fr/(0.5*p1), p1))
    _VARS['window']['-lbl2-'].update(" R1: {} ohm, R2:{} ohm, L1: {} H, L2: {} H".format(r1, r2, l1, l2))

    if values['-CASE1-']:               # Variable Frequency
        f = [20, 30, 40, 50, 60, 70, 80]
        for i in range(len(f)):
            x1 = 2 * 3.14 * f[i] * l1
            x2 = 2 * 3.14 * f[i] * l2
            ns = 60 * f[i] / (0.5*p1)
            n = (1 - s) * ns
            Ws = (2 * 3.14 * ns) / 60
            T = (3 * (Vs ** 2) / Ws) * ((r2 / s) / ((r1 + r2 / s) ** 2 + (x1 + x2) ** 2))
            Tm = (3 * Vs ** 2 / (2 * Ws)) * 1 / (r1 + np.sqrt((r1) ** 2 + ((x1 + x2) ** 2)))
            plt.text(ns, Tm, int(Tm))
            plt.plot(n, T, label="f= {}".format(f[i]))

    if values['-CASE2-']:               # Pole Changer
        p2 = int(values['p2'])
        if p2 % 2 != 0:
            raise Exception
        poleSelect = [p1, p2]
        for p in poleSelect:
            x1 = 2 * 3.14 * fr * l1
            x2 = 2 * 3.14 * fr * l2
            ns = (60 * fr) / (0.5*p)
            n = (1 - s) * ns
            Ws = (2 * 3.14 * ns) / 60
            T = ((3 * Vs ** 2) / Ws) * ((r2 / s) / (((r1 + r2 / s) ** 2) + ((x1 + x2) ** 2)))
            Tm = (3 * Vs ** 2 / (2 * Ws)) * 1 / (r1 + np.sqrt((r1) ** 2 + ((x1 + x2) ** 2)))
            plt.text(ns, Tm, int(Tm))
            plt.plot(n, T, label="P= {}".format(p))

    if values['-CASE3-']:                # V/f Operation
        f = [20, 30, 40, 50, 60, 70, 80]
        for i in range(len(f)):
            x1 = 2 * 3.14 * f[i] * l1
            x2 = 2 * 3.14 * f[i] * l2
            ns = 60 * f[i] / (0.5*p1)
            n = (1 - s) * ns
            Ws = (2 * 3.14 * ns) / 60
            if f[i] <= fr:               # First region where Torque is constant. (given that we neglect stator resistance)
                Vn = (Vs / fr) * f[i]
                T = (3 * Vn ** 2 / Ws) * ((r2 / s) / ((r1 + r2 / s) ** 2 + (x1 + x2) ** 2))
                Tm = (3 * Vs ** 2 / (2 * Ws)) * 1 / (r1 + np.sqrt((r1) ** 2 + ((x1 + x2) ** 2)))
                plt.text(ns, Tm, int(Tm))
                plt.plot(n, T, label="f= {}".format(f[i]))
            else:                       # Second region where torque starts to decrease.
                T = (3 * (Vs ** 2) / Ws) * ((r2 / s) / ((r1 + r2 / s) ** 2 + (x1 + x2) ** 2))
                Tm = (3 * Vs ** 2 / (2 * Ws)) * 1 / (r1 + np.sqrt((r1) ** 2 + ((x1 + x2) ** 2)))
                plt.text(ns, Tm, int(Tm))
                plt.plot(n, T, label="f= {}".format(f[i]))

    plt.xlabel('Speed n (RPM)')
    plt.ylabel('Torque (N.m)')
    plt.title('T-S Characteristics')
    plt.legend()
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


# MAIN LOOP
empty_plot()
while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == 'Draw':
        try:
            plt.clf()
            drawChart()
        except Exception:
            empty_plot()
            sg.Popup('Please make sure you\'ve selected a mode of operation and selected/'
                     'entered the required machine specs with even number of poles.'
                     , title='Error', font=AppFont)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

_VARS['window'].close()
