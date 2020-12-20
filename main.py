import PySimpleGUI as sg
from classes import *

clients_array = []
cars_array = []
invoices_array = []

c1 = Client("Klaudia", "Wawoczny", 666)
c2 = Client("Sebastian", "Jarosz", 878)

clients_array.append(c1)
clients_array.append(c2)

i1 = Invoice(c1, 100)
i2 = Invoice(c2, 69, True)

invoices_array.append(i1)
invoices_array.append(i2)

# Event names
ADD_CLIENT_EVENT = "-addClient-"
REMOVE_CLIENT_EVENT = "-removeClient-"
SAVE_CLIENT_EVENT = "-saveClient-"
CANCEL_CLIENT_EVENT = "-cancelClient-"
ADD_CAR_EVENT = "-addCar-"
REMOVE_CAR_EVENT = "-removeCar-"
ADD_INVOICE_EVENT = "-addInvoice-"
REMOVE_INVOICE_EVENT = "-removeInvoice-"
EXIT_EVENT = '-exit-'

# Fields keys
FIRST_NAME_FIELD = '-firstName-'
LAST_NAME_FIELD = '-lastName-'
PHONE_NUMBER_FIELD = '-phoneNumber-'
CLIENTS_LIST_FIELD = '-clientsList-'

clients_tab = [[sg.Text("PANEL KLIENTÓW")],
               [sg.Listbox(values=clients_array, size=(800, 20), key=CLIENTS_LIST_FIELD)],
               [sg.ReadButton("Dodaj klienta", key=ADD_CLIENT_EVENT),
                sg.ReadButton("Usuń klienta", key=REMOVE_CLIENT_EVENT)]]

cars_tab = [[sg.Text("PANEL SAMOCHODÓW")],
            [sg.Listbox(values=cars_array, size=(800, 20))],
            [sg.ReadButton("Dodaj samochód", key=ADD_CAR_EVENT), sg.ReadButton("Usuń samochód", key=REMOVE_CAR_EVENT)]]

invoices_tab = [[sg.Text("PANEL FAKTUR")],
                [sg.Listbox(values=invoices_array, size=(800, 20))],
                [sg.ReadButton("Dodaj fakturę", key=ADD_INVOICE_EVENT),
                 sg.ReadButton("Usuń fakturę", key=REMOVE_INVOICE_EVENT)]]

main_window_layout = [[sg.TabGroup([[sg.Tab("Klienci", clients_tab)],
                                    [sg.Tab("Samochody", cars_tab)],
                                    [sg.Tab("Faktury", invoices_tab)]])],
                      [sg.Exit("Wyjście", key=EXIT_EVENT)]]

add_client_window_layout = [[sg.Text("Imię "), sg.InputText(key=FIRST_NAME_FIELD)],
                            [sg.Text("Nazwisko "), sg.InputText(key=LAST_NAME_FIELD)],
                            [sg.Text("Numer Telefonu "), sg.InputText(key=PHONE_NUMBER_FIELD)],
                            [sg.ReadButton("Zapisz", key=SAVE_CLIENT_EVENT), sg.ReadButton("Anuluj", key=CANCEL_CLIENT_EVENT)]]

running = True
client_window_active = False
client_window = None


def add_client_window_func():
    global client_window_active
    global client_window

    client_window_event, client_window_values = client_window.read()
    print("Client window event invoked: " + client_window_event)

    if client_window_event == SAVE_CLIENT_EVENT:
        print(client_window_values)
        is_client_data_valid = validate_client_window(client_window_values)
        print("is valid: " + str(is_client_data_valid))

        if is_client_data_valid:
            new_client = Client(client_window_values[FIRST_NAME_FIELD], client_window_values[LAST_NAME_FIELD],
                                client_window_values[PHONE_NUMBER_FIELD])

            clients_array.append(new_client)
            client_window_active = False
            client_window.hide()

            main_window[CLIENTS_LIST_FIELD].update(clients_array)
            main_window.UnHide()
        else:
            sg.Popup("All client fields must be fulfilled", non_blocking=True)

    if client_window_event == CANCEL_CLIENT_EVENT or client_window_event == sg.WIN_CLOSED:
        client_window_active = False
        client_window.hide()
        main_window.UnHide()


def clear_client_window_fields():
    global client_window

    client_window[FIRST_NAME_FIELD].update("")
    client_window[LAST_NAME_FIELD].update("")
    client_window[PHONE_NUMBER_FIELD].update("")


def validate_client_window(client_window_values):
    first_name = client_window_values[FIRST_NAME_FIELD]
    last_name = client_window_values[LAST_NAME_FIELD]
    phone_number = client_window_values[PHONE_NUMBER_FIELD]

    return bool(first_name and last_name and phone_number)


main_window = sg.Window("Warsztat Samochodowy Python", main_window_layout, size=(1000, 400))

while running:
    main_window_event, main_window_values = main_window.read()
    print("Main window event invoked: " + main_window_event)

    if main_window_event == sg.WIN_CLOSED or main_window_event == EXIT_EVENT:
        break

    if main_window_event == REMOVE_CLIENT_EVENT:
        print("Remove client: " + str(main_window_values[CLIENTS_LIST_FIELD]))

        # Listbox values are returned as array so there is a need to take first element from array
        removed_client = main_window_values[CLIENTS_LIST_FIELD][0] if len(main_window_values[CLIENTS_LIST_FIELD]) > 0 \
            else None

        if removed_client is not None:
            clients_array.remove(removed_client)
            main_window[CLIENTS_LIST_FIELD].update(clients_array)

    if not client_window_active and main_window_event == ADD_CLIENT_EVENT:
        main_window.hide()
        client_window_active = True

        # if added to prevent from layout "re-usage" exception
        if client_window is None:
            client_window = sg.Window("Warsztat Samochodowy Python - Dodaj klienta", add_client_window_layout,
                                      size=(500, 400))
        else:
            clear_client_window_fields()
            client_window.un_hide()

        while client_window_active:
            add_client_window_func()

print("App closed")
main_window.close()
