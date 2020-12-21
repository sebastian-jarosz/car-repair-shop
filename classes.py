from datetime import *


class Client:
    def __init__(self, first_name, last_name, phone_number, car=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.cars = []
        if car is not None:
            self.cars.append(car)

    def __repr__(self):
        return "IMIĘ: " + self.first_name + " " + \
               "NAZWISKO: " + self.last_name + " " + \
               "NR.TEL.: " + str(self.phone_number) + " " + \
               "ILOŚĆ SAMOCHODÓW: " + str(len(self.cars))

    def add_car(self, car):
        if car is not None:
            self.cars.append(car)

    def remove_car(self, car):
        if car is not None:
            self.cars.remove(car)

    def get_name(self):
        return self.first_name + " " + self.last_name


class Car:
    def __init__(self, make, model, reg_number, owner=None):
        self.make = make
        self.model = model
        self.reg_number = reg_number
        self.owner = owner
        if owner is not None:
            owner.add_car(self)

    def __repr__(self):
        return "MARKA: " + self.make + " " + \
               "MODEL: " + self.model + " " + \
               "NR.REJ.: " + self.reg_number + \
               ((" WŁAŚCICIEL: " + str(self.owner.get_name())) if self.owner is not None else "")


class Invoice:
    now = datetime.now()
    invoice_number_beginning = "FKT/VAT/" + str(now.year) + "/" + str(now.month) + "/REF-"

    def __init__(self, client, amount, is_paid=None):
        self.number = self.invoice_number_beginning + str(id(self))
        self.client = client
        self.amount = amount
        if is_paid is not None:
            self.is_paid = is_paid
        else:
            self.is_paid = False

    def __repr__(self):
        return "Numer faktury: " + self.number + " " + \
               "Klient: " + str(self.client) + " " + \
               "Kwota: " + str(self.amount) + " " + \
               "Opłacona: " + str(self.is_paid)

