import csv
from typing import NamedTuple


class Smartphone(NamedTuple):
    name: str
    cpu: float
    ram: int
    storage: int
    camera: int
    battery: int
    weight: int
    price: int

    def __ge__(self, other):
        if isinstance(other, Smartphone):
            return (
                self.cpu >= other.cpu
                and self.ram >= other.ram
                and self.storage >= other.storage
                and self.camera >= other.camera
                and self.battery >= other.battery
                and self.weight <= other.weight
                and self.price <= other.price
            )
        else:
            raise ValueError("Comparison with unsupported type.")


smartphones = []

with open(file="data.csv", mode="r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for r in reader:
        phone = Smartphone(*r)  # type: ignore
        smartphones.append(phone)

for s1 in smartphones:
    for s2 in smartphones:
        if s1 >= s2 and s1.name != s2.name:
            print(f"({s1.name}) dominate ({s2.name})")
