import PySimpleGUI as sg
from classes import *
from constants import *

clients_array = []
cars_array = []
invoices_array = []

# Init example data
c1 = Client("Klaudia", "W", 666)
c2 = Client("Sebastian", "J", 878)
clients_array.append(c1)
clients_array.append(c2)
car1 = Car("Chevy", "Cruze", "WA1234")
car2 = Car("Opel", "Astra", "WY1234")
cars_array.append(car1)
cars_array.append(car2)
i1 = Invoice(c1, 100)
i2 = Invoice(c2, 69, True)
invoices_array.append(i1)
invoices_array.append(i2)

# Layouts
clients_tab = [[sg.Text("PANEL KLIENTÓW")],
               [sg.Listbox(values=clients_array, size=(800, 20), key=CLIENTS_LIST_FIELD)],
               [sg.ReadButton("Dodaj klienta", key=ADD_CLIENT_EVENT),
                sg.ReadButton("Usuń klienta", key=REMOVE_CLIENT_EVENT)]]

cars_tab = [[sg.Text("PANEL SAMOCHODÓW")],
            [sg.Listbox(values=cars_array, size=(800, 20), key=CARS_LIST_FIELD)],
            [sg.ReadButton("Dodaj samochód", key=ADD_CAR_EVENT), sg.ReadButton("Usuń samochód", key=REMOVE_CAR_EVENT)]]

invoices_tab = [[sg.Text("PANEL FAKTUR")],
                [sg.Listbox(values=invoices_array, size=(800, 20), key=INVOICES_LIST_FIELD)],
                [sg.ReadButton("Dodaj fakturę", key=ADD_INVOICE_EVENT),
                 sg.ReadButton("Usuń fakturę", key=REMOVE_INVOICE_EVENT)]]

main_window_layout = [[sg.TabGroup([[sg.Tab("Klienci", clients_tab)],
                                    [sg.Tab("Samochody", cars_tab)],
                                    [sg.Tab("Faktury", invoices_tab)]])],
                      [sg.Exit("Wyjście", key=EXIT_EVENT)]]

add_client_window_layout = [[sg.Text("Imię "), sg.InputText(key=FIRST_NAME_FIELD)],
                            [sg.Text("Nazwisko "), sg.InputText(key=LAST_NAME_FIELD)],
                            [sg.Text("Numer Telefonu "), sg.InputText(key=PHONE_NUMBER_FIELD)],
                            [sg.ReadButton("Zapisz", key=SAVE_CLIENT_EVENT),
                             sg.ReadButton("Anuluj", key=CANCEL_CLIENT_EVENT)]]

add_car_window_layout = [[sg.Text("Marka "), sg.InputText(key=MAKE_FIELD)],
                         [sg.Text("Model "), sg.InputText(key=MODEL_FIELD)],
                         [sg.Text("Nr Rej. "), sg.InputText(key=REG_NUMBER_FIELD)],
                         [sg.Text("Właściciel "), sg.Combo(values=clients_array, readonly=True, key=OWNER_FIELD)],
                         [sg.ReadButton("Zapisz", key=SAVE_CAR_EVENT), sg.ReadButton("Anuluj", key=CANCEL_CAR_EVENT)]]

add_invoice_window_layout = [[sg.Text("Klient "), sg.Combo(values=clients_array, readonly=True, key=CLIENT_FIELD)],
                             [sg.Text("Kwota "), sg.InputText(key=AMOUNT_FIELD)],
                             [sg.Checkbox("Opłacono? ", key=IS_PAID_FIELD)],
                             [sg.ReadButton("Zapisz", key=SAVE_INVOICE_EVENT),
                              sg.ReadButton("Anuluj", key=CANCEL_INVOICE_EVENT)]]

running = True
client_window_active = False
client_window = None
car_window_active = False
car_window = None
invoice_window_active = False
invoice_window = None

main_window = sg.Window("Warsztat Samochodowy Python", main_window_layout, size=(1000, 400))


# Functions - Client
def add_client_window_func():
    global client_window_active
    global client_window

    client_window_event, client_window_values = client_window.read()
    print("Client window event invoked: " + str(client_window_event))

    if client_window_event == SAVE_CLIENT_EVENT:
        is_client_data_valid = validate_client_window(client_window_values)

        if is_client_data_valid:
            new_client = Client(client_window_values[FIRST_NAME_FIELD],
                                client_window_values[LAST_NAME_FIELD],
                                client_window_values[PHONE_NUMBER_FIELD])

            clients_array.append(new_client)
            client_window_active = False
            client_window.hide()

            main_window[CLIENTS_LIST_FIELD].update(clients_array)
            main_window.UnHide()
        else:
            sg.Popup("Wszystkie dane klienta muszą być uzupełnione", non_blocking=True)

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


def remove_client():
    print("Remove client: " + str(main_window_values[CLIENTS_LIST_FIELD]))

    # Listbox values are returned as array so there is a need to take first element from array
    removed_client = main_window_values[CLIENTS_LIST_FIELD][0] \
        if len(main_window_values[CLIENTS_LIST_FIELD]) > 0 else None

    if removed_client is not None:
        clients_array.remove(removed_client)
        main_window[CLIENTS_LIST_FIELD].update(clients_array)


def add_car_window_func():
    global car_window_active
    global car_window

    car_window_event, car_window_values = car_window.read()
    print("Car window event invoked: " + str(car_window_event))

    if car_window_event == SAVE_CAR_EVENT:
        is_car_data_valid = validate_car_window(car_window_values)

        if is_car_data_valid:
            new_car = Car(car_window_values[MAKE_FIELD],
                          car_window_values[MODEL_FIELD],
                          car_window_values[REG_NUMBER_FIELD],
                          # check cause - sg returning "" when value is not selected in Combo
                          car_window_values[OWNER_FIELD] if car_window_values[OWNER_FIELD] else None)

            cars_array.append(new_car)
            car_window_active = False
            car_window.hide()

            main_window[CARS_LIST_FIELD].update(cars_array)
            # Clients list also needs to be updated to show proper values
            main_window[CLIENTS_LIST_FIELD].update(clients_array)
            main_window.UnHide()
        else:
            sg.Popup("Wszystkie dane samochodu muszą być uzupełnione", non_blocking=True)

    if car_window_event == CANCEL_CLIENT_EVENT or car_window_event == sg.WINDOW_CLOSED:
        car_window_active = False
        car_window.hide()
        main_window.UnHide()


def clear_car_window_fields():
    global car_window

    car_window[MAKE_FIELD].update("")
    car_window[MODEL_FIELD].update("")
    car_window[REG_NUMBER_FIELD].update("")
    car_window[OWNER_FIELD].update("")
    car_window[OWNER_FIELD].update(values=clients_array)


def validate_car_window(car_window_values):
    make = car_window_values[MAKE_FIELD]
    model = car_window_values[MODEL_FIELD]
    reg_number = car_window_values[REG_NUMBER_FIELD]
    owner = car_window_values[OWNER_FIELD]

    return bool(make and model and reg_number and owner)


def remove_car():
    print("Remove car: " + str(main_window_values[CARS_LIST_FIELD]))

    # Listbox values are returned as array so there is a need to take first element from array
    removed_car = main_window_values[CARS_LIST_FIELD][0] \
        if len(main_window_values[CARS_LIST_FIELD]) > 0 else None

    if removed_car is not None:
        cars_array.remove(removed_car)
        main_window[CARS_LIST_FIELD].update(cars_array)

        if removed_car.owner is not None:
            removed_car.owner.remove_car(removed_car)
            main_window[CLIENTS_LIST_FIELD].update(clients_array)


def add_invoice_window_func():
    global invoice_window_active
    global invoice_window

    invoice_window_event, invoice_window_values = invoice_window.read()
    print("Invoice window event invoked: " + str(invoice_window_event))

    if invoice_window_event == SAVE_INVOICE_EVENT:
        is_invoice_data_valid = validate_invoice_window(invoice_window_values)

        if is_invoice_data_valid:
            new_invoice = Invoice(invoice_window_values[CLIENT_FIELD], invoice_window_values[AMOUNT_FIELD],
                                  invoice_window_values[IS_PAID_FIELD])

            invoices_array.append(new_invoice)
            invoice_window_active = False
            invoice_window.hide()

            main_window[INVOICES_LIST_FIELD].update(invoices_array)
            main_window.UnHide()
        else:
            sg.Popup("Wszystkie dane dla nowej faktury muszą być uzupełnione", non_blocking=True)

    if invoice_window_event == CANCEL_INVOICE_EVENT or invoice_window_event == sg.WINDOW_CLOSED:
        invoice_window_active = False
        invoice_window.hide()
        main_window.UnHide()


def clear_invoice_window_fields():
    global invoice_window

    invoice_window[CLIENT_FIELD].update("")
    invoice_window[CLIENT_FIELD].update(values=clients_array)
    invoice_window[AMOUNT_FIELD].update("")
    invoice_window[IS_PAID_FIELD].update("")


def validate_invoice_window(invoice_window_values):
    client = invoice_window_values[CLIENT_FIELD]
    amount = invoice_window_values[AMOUNT_FIELD]
    is_paid = invoice_window_values[CLIENT_FIELD]

    return bool(client and amount and is_paid)


def remove_invoice():
    print("Remove car: " + str(main_window_values[INVOICES_LIST_FIELD]))

    # Listbox values are returned as array so there is a need to take first element from array
    removed_invoice = main_window_values[INVOICES_LIST_FIELD][0] \
        if len(main_window_values[INVOICES_LIST_FIELD]) > 0 else None

    if removed_invoice is not None:
        invoices_array.remove(removed_invoice)
        main_window[INVOICES_LIST_FIELD].update(invoices_array)


while running:
    main_window_event, main_window_values = main_window.read()
    print("Main window event invoked: " + str(main_window_event))

    if main_window_event == sg.WIN_CLOSED or main_window_event == EXIT_EVENT:
        break

    # Remove client - main window
    if main_window_event == REMOVE_CLIENT_EVENT:
        remove_client()

    # Add client - separate window
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

    # Remove car - main window
    if main_window_event == REMOVE_CAR_EVENT:
        remove_car()

    # Add car - separate window
    if not car_window_active and main_window_event == ADD_CAR_EVENT:
        main_window.hide()
        car_window_active = True

        # if added to prevent from layout "re-usage" exception
        if car_window is None:
            car_window = sg.Window("Warsztat Samochodowy Python - Dodaj samochód", add_car_window_layout,
                                   size=(500, 400))
        else:
            clear_car_window_fields()
            car_window.un_hide()

        while car_window_active:
            add_car_window_func()

    # Remove invoice - main window
    if main_window_event == REMOVE_INVOICE_EVENT:
        remove_invoice()

    # Add invoice - separate window
    if not invoice_window_active and main_window_event == ADD_INVOICE_EVENT:
        main_window.hide()
        invoice_window_active = True

        # if added to prevent from layout "re-usage" exception
        if invoice_window is None:
            invoice_window = sg.Window("Warsztat Samochodowy Python - Dodaj fakturę", add_invoice_window_layout,
                                       size=(500, 400))
        else:
            clear_invoice_window_fields()
            invoice_window.un_hide()

        while invoice_window_active:
            add_invoice_window_func()

print("Warsztat Samochodowy Python - Application closed")
main_window.close()
