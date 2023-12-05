# import random
# import datetime

# res = str(hex(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))
# capitalized_res = res[2:][::-1]

# print(capitalized_res, type(capitalized_res))

import random

def generatePrivateUniqueId(adder=""):
    characters = 'qwertyuiopasdfghjklzxcvbnm' + '1234567890'
    unique_id = ''.join(random.choices(characters, k=10))
    if len(adder) > 0:
        return adder+"-"+unique_id
    else:
        return unique_id

# Example usage:
# user_id = generatePrivateUniqueId()
# print(generatePrivateUniqueId(), generatePrivateUniqueId("accId"))

# print(generatePrivateUniqueId("imageId"))




