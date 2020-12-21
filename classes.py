from datetime import *


class Client:
    def __init__(self, first_name, last_name, phone_number, car=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.cars = []
        self.cars.append(car) if car is not None else None

    def __repr__(self):
        return "Imię: " + self.first_name + " " + \
               "Nazwisko: " + self.last_name + " " + \
               "Nr.Tel.: " + str(self.phone_number) + " " + \
               "Ilość samochodów: " + str(len(self.cars))

    def add_car(self, car):
        self.cars.append(car)
        car.add_owner(self)


class Car:
    def __init__(self, make, model, reg_number, owner=None):
        self.make = make
        self.model = model
        self.reg_number = reg_number
        self.owner = owner if owner is not None else None

    def __repr__(self):
        return "Marka: " + self.make + " " + \
               "Model: " + self.model + " " + \
               "Nr.Rej.: " + self.reg_number

    def add_owner(self, owner):
        self.owner = owner


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

