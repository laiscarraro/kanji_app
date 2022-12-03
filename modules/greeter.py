import re
import pandas as pd

class Greeter():

    def __init__(self):
        self.greetings = pd.read_csv('data/greetings.csv', sep=';')
    
    def replace_name(self, greeting, user):
        return re.sub('NOME', user.get_name(), greeting)

    def greet(self, user):
        greeting = self.greetings.sample().greeting
        return self.replace_name(
            greeting.values[0], user
        )