from template_generator import producer


# products = {"cable": 3,
#             "mixer": 150,
#             "headphones": 50,
#             "guitar": 75,
#             "piano": 250,
#             "microphone": 60,
#             "speaker": 94,
#             "accesories": 17,
#             "violin": 230,
#             "trumpet": 200,
#             "books": 5,
#             "notes": 6,
#             "xylophones": 164
#             }

products = {"test": 1}

for entry in products.keys():
    producer(entry, products[entry], str(entry + ".template"))
