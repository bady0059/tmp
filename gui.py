import PySimpleGUI as sg
import time
import threading


class GUI():
    
    def loading(self, time):
        layout =  [[sg.Text('wainting...', size=(50, 1), relief='sunken', font=('Courier', 11),text_color='yellow', background_color='black',key='TEXT')]]
        window = sg.Window("loading", layout)

        while True:
            event, values = window.read(timeout=time, close=True)
            if event == sg.WIN_CLOSED:
                break

        window.close()
    
    def get_window(self):
        return self.window()

    def show_aps(self, data):


        headings = ['SSID', 'mac', 'channel', 'company']

        layout = [[sg.Table(values=data, headings=headings, max_col_width=35,
                            background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='left',
                            num_rows=20,
                            key='_rowselected_',
                            row_height=35,
                            tooltip='This is a table')],
                [sg.Button('Attack')],
                [sg.Text('Attack = start half handshake attack')]]
                
                
        window = sg.Window('The Table Element', layout )

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == 'Attack':
                window.close()
                return int(values['_rowselected_'][0])

        window.close()

    
    def half_handshake(self):

        layout = [[sg.Text("", size=(50, 5), key='OUTPUT')],[sg.Button('Done')]]

        self.window = sg.Window("find password", layout)

        while True:
            
            event, values = self.window.read(timeout = 1000)
            if event == sg.WINDOW_CLOSED or event == 'Done':
                break      
            
        self.window.close()
    
    def display(self, message):
        self.window['OUTPUT'].update(value=message)
        
    def choose_file(self):
    
        layout = [[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],
            [sg.FileBrowse(target='_FILEBROWSE_')],
            [sg.OK()]]

        self.window = sg.Window("choose password file", layout)

        while True:
            
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == "_FILEBROWSE_":
                self.window.close()
                print(values['_FILEBROWSE_']) 
                return values['_FILEBROWSE_']    
            
        self.window.close()
    
    def inside_wifi(self, data):


        headings = ['mac', 'ip', 'name', 'company']

        layout = [[sg.Table(values=data, headings=headings, max_col_width=35,
                            background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='left',
                            num_rows=20,
                            key='_rowselected_',
                            row_height=35,
                            tooltip='This is a table')],
                [sg.Button('scan ports')],
                [sg.Button('mitm')],
                [sg.Button('dns spoof')]]
                
                
        window = sg.Window('The Table Element', layout )

        while True:
            event, values = window.read()
            
            if event:
                window.close()
                if event == sg.WIN_CLOSED:
                    return "close", Device("")
                elif event == 'scan ports':
                    return 'scan ports',int(values['_rowselected_'][0])
                elif event == 'mitm':
                    return 'mitm',int(values['_rowselected_'][0])
                elif event == 'dns spoof':
                    return 'dns spoof',int(values['_rowselected_'][0])
    
    def scan_ports(self):
    
        layout = [[sg.Text("", size=(50, 5), key='OUTPUT')],[sg.Button('Done')]]

        self.window = sg.Window("scan ports", layout)

        while True:
            
            event, values = self.window.read(timeout = 1000)
            if event == sg.WINDOW_CLOSED or event == 'Done':
                
                break      
            
        self.window.close()

    def mitm(self):
    
        layout = [[sg.Text("", size=(50, 5), key='OUTPUT')],[sg.Button('Stop')]]

        self.window = sg.Window("mitm", layout)

        while True:
            
            event, values = self.window.read(timeout = 1000)
            if event == sg.WINDOW_CLOSED or event == 'Stop':
                
                break      
            
        self.window.close()    
        
    def dns_spoof(self):
    
        layout = [[sg.Text("", size=(50, 5), key='OUTPUT')],[sg.Button('Stop')]]

        self.window = sg.Window("dns spoof", layout)

        while True:
            
            event, values = self.window.read(timeout = 1000)
            if event == sg.WINDOW_CLOSED or event == 'Stop':
                
                break      
            
        self.window.close()  

    def input(self):
                
        layout = [[sg.Text('domain: ', size =(15, 1)), sg.InputText()],[sg.Button('Attack')]]

        window = sg.Window("input", layout)

        while True:
            
            event, values = window.read(timeout = 1000)
            if event == sg.WINDOW_CLOSED or event == 'Attack':
                window.close()
                return values[0]
                break      
                
        window.close() 

        
