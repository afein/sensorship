ports = {
    "analog" :
        {
            "A0": 0,
            "A1": 1,
            "A2": 2
        },
    "digital" :
        {
            "D2": 2,
            "D3": 3,
            "D4": 4,
            "D5": 5,
            "D6": 6,
            "D7": 7,
            "D8": 8,
            "A0": 14,
            "A1": 15,
            "A2": 16
        }
}

devices = {
    "grove_button" : {"sensor_type" : "digital", "units" : "pressed"},
    "grove_light" : {"sensor_type" : "analog", "units" : "lux"},
    "grove_rotary_angle" : {"sensor_type" : "analog", "units" : "degrees"},
    "grove_sound" : {"sensor_type" : "analog", "units" : "ADC"},
    "grove_temperature" : {"sensor_type" : "analog", "units" : "Celcius"},
    "grove_touch" : {"sensor_type" : "digital", "units" : "pressed"}
}

