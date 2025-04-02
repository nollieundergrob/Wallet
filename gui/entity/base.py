from sys import stdout
class BaseEntity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def display(self):
        stdout.write(f"\nName: {self.name}\n")
        stdout.write(f"Description: {self.description}\n")