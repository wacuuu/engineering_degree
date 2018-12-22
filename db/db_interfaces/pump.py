from db_pump import producer

quantities = {
#     "../template_generation/accesories.template": 1000,
#     "../template_generation/books.template": 10000,
     "../template_generation/cable.template": 10000,
#     "../template_generation/guitar.template": 1000,
#     "../template_generation/headphones.template": 1000,
#     "../template_generation/microphone.template": 600,
#     "../template_generation/mixer.template": 100,
#     "../template_generation/notes.template": 10000,
#     "../template_generation/piano.template": 100,
#    "../template_generation/speaker.template": 500,
#    "../template_generation/trumpet.template": 100,
#    "../template_generation/violin.template": 100,
#    "../template_generation/xylophones.template": 100
}
# quantities = {
#     "../template_generation/piano.template": 1
# }
producer(quantities)
