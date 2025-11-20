import threading

class VehicleData:
    def __init__(self):
        self._lock = threading.Lock()

        # lights and blinker
        self._highbeam = False
        self._lowbeam = False
        self._standlight = False
        self._left_blinker = False
        self._right_blinker = False
        self._hazard = False
        self._interior_light = False

        # gear and speed
        self._gear = 126 # P
        self._speed = 0

        # person detection
        self._person_detected = False
        self._person_distance = 0

        # Doors
        self._door_status = 0

        # Parksensor
        self._parksensor_active = False
        self._parksensor_level = 0
        self._parksensor_distance = 0

        # Fuel level and odometer
        self._fuel_level = 0
        self._info_cnt = 0  # to switch between fuel range and odometer
        self._fuel_range = 0
        self._odometer = 0

    # Setter und Getter with thread safety 
    # lock lets only one thread access the data at a time

    def set_highbeam(self, value: bool):
        with self._lock:
            self._highbeam = value

    def get_highbeam(self):
        with self._lock:
            return self._highbeam

    def set_lowbeam(self, value: bool):
        with self._lock:
            self._lowbeam = value

    def get_lowbeam(self):
        with self._lock:
            return self._lowbeam

    def set_standlight(self, value: bool):
        with self._lock:
            self._standlight = value

    def get_standlight(self):
        with self._lock:
            return self._standlight

    def set_interior_light(self, value: bool):
        with self._lock:
            self._interior_light = value

    def get_interior_light(self):
        with self._lock:
            return self._interior_light

    def set_left_blinker(self, value: bool):
        with self._lock:
            self._left_blinker = value

    def get_left_blinker(self):
        with self._lock:
            return self._left_blinker

    def set_right_blinker(self, value: bool):
        with self._lock:
            self._right_blinker = value

    def get_right_blinker(self):
        with self._lock:
            return self._right_blinker

    def set_hazard(self, value: bool):
        with self._lock:
            self._hazard = value

    def get_hazard(self):
        with self._lock:
            return self._hazard

    def set_gear(self, gear: int):
        with self._lock:
            self._gear = gear

    def get_gear(self):
        with self._lock:
            return self._gear

    def set_speed(self, speed: int):
        with self._lock:
            self._speed = speed

    def get_speed(self):
        with self._lock:
            return self._speed

    def set_person_detected(self, value: bool):
        with self._lock:
            self._person_detected = value

    def get_person_detected(self):
        with self._lock:
            return self._person_detected

    def set_person_distance(self, distance: int):
        with self._lock:
            self._person_distance = distance

    def get_person_distance(self):
        with self._lock:
            return self._person_distance

    def set_door_status(self, status: int):
        with self._lock:
            self._door_status = status

    def get_door_status(self):
        with self._lock:
            return self._door_status

    def set_parksensor_level(self, level: int):
        with self._lock:
            self._parksensor_level = level

    def get_parksensor_level(self):
        with self._lock:
            return self._parksensor_level

    def set_parksensor_active(self, value: bool):
        with self._lock:
            self._parksensor_active = value

    def get_parksensor_active(self):
        with self._lock:
            return self._parksensor_active

    def set_parksensor_distance(self, value: int):
        with self._lock:
            self._parksensor_distance = value

    def get_parksensor_distance(self):
        with self._lock:
            return self._parksensor_distance

    def set_fuel_level(self, level: int):
        with self._lock:
            self._fuel_level = level

    def get_fuel_level(self):
        with self._lock:
            return self._fuel_level

    def set_info_cnt(self, value: bool):
        with self._lock:
            self._info_cnt = value

    def get_info_cnt(self):
        with self._lock:
            return self._info_cnt

    def toggle_info_cnt(self):
        self._info_cnt = not self._info_cnt

    def set_fuel_range(self, fuel_range: float):
        with self._lock:
            self._fuel_range = fuel_range

    def get_fuel_range(self):
        with self._lock:
            return self._fuel_range

    def set_odometer(self, odometer: float):
        with self._lock:
            self._odometer = odometer

    def get_odometer(self):
        with self._lock:
            return self._odometer
