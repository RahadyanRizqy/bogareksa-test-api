import random

def generatePrivateUniqueId(adder=""):
    characters = 'qwertyuiopasdfghjklzxcvbnm' + '1234567890'
    unique_id = ''.join(random.choices(characters, k=10))
    return adder+"-"+unique_id if len(adder) > 0 else unique_id