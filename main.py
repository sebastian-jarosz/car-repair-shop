import PySimpleGUI as sg
from classes import *

clients = []
cars = []
invoices = []

c1 = Client("Klaudia", "Wawoczny", 666)
c2 = Client("Sebastian", "Jarosz", 878)

clients.append(c1)
clients.append(c2)

i1 = Invoice(c1, 100)
i2 = Invoice(c2, 69, True)

invoices.append(i1)
invoices.append(i2)

clients_tab = [[sg.Text("PANEL KLIENTÓW")],
               [sg.Listbox(values=clients, size=(100, 10))],
               [sg.ReadButton("Dodaj klienta"), sg.ReadButton("Usuń klienta")]]

cars_tab = [[sg.Text("PANEL SAMOCHODÓW")],
            [sg.Listbox(values=cars, size=(100, 10))],
            [sg.ReadButton("Dodaj samochód"), sg.ReadButton("Usuń samochód")]]

invoices_tab = [[sg.Text("PANEL FAKTUR")],
            [sg.Listbox(values=invoices, size=(100, 10))],
            [sg.ReadButton("Dodaj fakturę"), sg.ReadButton("Usuń fakturę")]]

layout = [[sg.TabGroup([[sg.Tab("Klienci", clients_tab)],
                        [sg.Tab("Samochody", cars_tab)],
                        [sg.Tab("Faktury", invoices_tab)]])],
          [sg.Exit("Wyjście")]]

# 2 - the window

window = sg.Window('Warsztat Samochodowy Python', layout)

# 3 - the read
event, values = window.read()

# 4 - the close
window.close()