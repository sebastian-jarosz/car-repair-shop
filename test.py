from classes import *


car = Car("Chevrolet", "Cruze", "SI69000")
car1 = Car("BMW", "Cruze", "SI69000")
client = Client("Sebastian", "Jarosz", 793079995, car)

client.add_car(car1)
# print(client.first_name)
# print(client.cars)
# print(car1)
# print(car)
print(car1.owner)