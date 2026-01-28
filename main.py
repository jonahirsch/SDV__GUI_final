import sys
import threading
import time
import keyboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui import SDV_UI
from vehicle_data import VehicleData
from kuksa_client.grpc import VSSClient, Datapoint


def input_thread(data: VehicleData, ui: SDV_UI):
    ### Input Thread ###
    try:
        kuksa_client = VSSClient('localhost', 55555)
        kuksa_client.connect()
        print("Kuksa Databroker connected successfully")
    except Exception as e:
        print("Kuksa connection failed: ", e)
        kuksa_client = None

    # Set-Signals
    SET_SIGNALS = {
        "highbeam": "Vehicle.Body.Lights.Beam.High.IsOn",
        "lowbeam": "Vehicle.Body.Lights.Beam.Low.IsOn",
        "standlight": "Vehicle.Body.Lights.IsOn",
        "hazard": "Vehicle.Body.Lights.Hazard.IsSignaling",
        "left": "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling",
        "right": "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling",
        "interior_light": "Vehicle.Cabin.Light.AmbientLight.IsLightOn"
    }

    # Read-Signals
    READ_SIGNALS = {
        "speed": "Vehicle.Speed", # in km/h
        "gear": "Vehicle.Powertrain.Transmission.CurrentGear", # 0=Neutral, 1/2/..=Forward, -1/-2/..=Reverse, 126=Park, 127=Drive
        "fuel_level": "Vehicle.Powertrain.FuelSystem.RelativeLevel", #fuel level realative (0%-100%)
        "fuel_range": "Vehicle.Powertrain.FuelSystem.Range", #fuel range in m"
        "odometer": "Vehicle.TraveledDistance", # mileage/odometer
        "door_left": "Vehicle.Cabin.Door.Row1.DriverSide.IsOpen",
        "door_right": "Vehicle.Cabin.Door.Row1.PassengerSide.IsOpen",
        "pdc_active": "Vehicle.ADAS.PDC.Rear.IsActive", 
        "pdc_distance": "Vehicle.ADAS.PDC.Rear.Distance", # in cm
        "person_detected": "Vehicle.ADAS.PD.Front.IsActive",
        "person_distance": "Vehicle.ADAS.PD.Front.Distance", # in cm
    }

    # Blinker timer
    blink_state = False
    last_blink_time = time.time()
    BLINK_INTERVAL = 1 / 1.5   # 1.5 Hz in s

    while True:
        # Read Kuksa-Data
        if kuksa_client:
            try:
                result = kuksa_client.get_current_values(list(READ_SIGNALS.values()))
                if result:
                    # Speed
                    speed = float(getattr(result.get(READ_SIGNALS["speed"]), "value",0.0))  # in km/h
                    data.set_speed(speed)

                    # Gear
                    gear = int(getattr(result.get(READ_SIGNALS["gear"]), "value", 0))
                    data.set_gear(gear)

                    # Fuel
                    fuel_level = float(getattr(result.get(READ_SIGNALS["fuel_level"]), "value", 100.0))
                    data.set_fuel_level(fuel_level)
                    fuel_range = float(getattr(result.get(READ_SIGNALS["fuel_range"]), "value", 0.0))  # in m
                    data.set_fuel_range(fuel_range / 1000)  # from m in km
                    odometer = float(getattr(result.get(READ_SIGNALS["odometer"]), "value", 0.0))  # in m
                    data.set_odometer(odometer / 1000)  # from m in km

                    # Doors
                    left_open = bool(getattr(result.get(READ_SIGNALS["door_left"]), "value", False))
                    right_open = bool(getattr(result.get(READ_SIGNALS["door_right"]), "value", False))
                    if left_open and right_open:
                        data.set_door_status(1)
                    elif left_open:
                        data.set_door_status(2)
                    elif right_open:
                        data.set_door_status(3)
                    else:
                        data.set_door_status(0)

                    # Parksensor
                    pdc_active = bool(getattr(result.get(READ_SIGNALS["pdc_active"]), "value", False))
                    data.set_parksensor_active(pdc_active)
                    dist = float(getattr(result.get(READ_SIGNALS["pdc_distance"]), "value", 0.0)) # in cm
                    data.set_parksensor_distance(int(dist))  # in cm
                    if dist <= 50:
                        data.set_parksensor_level(3)
                    elif dist <= 100:
                        data.set_parksensor_level(2)
                    elif dist <= 150:
                        data.set_parksensor_level(1)
                    else:
                        data.set_parksensor_level(0)

                    # Person Detection
                    person_detected = bool(getattr(result.get(READ_SIGNALS["person_detected"]), "value", False))
                    data.set_person_detected(person_detected)
                    person_distance = float(getattr(result.get(READ_SIGNALS["person_distance"]), "value", 0.0))  # in cm
                    data.set_person_distance(int(person_distance))  # in cm
                                        
            except Exception as e:
                print("Exception to read Kuksa-Data: ", e)

        # GUI-Button states to VehicleData
        data.set_highbeam(ui.highbeam_btn.isChecked())
        data.set_lowbeam(ui.lowbeam_btn.isChecked())
        data.set_standlight(ui.stand_light_btn.isChecked())
        data.set_interior_light(ui.interiorlight_btn.isChecked())
        
        now = time.time()

        # Blinker with 1.5 Hz
        active_btn = None
        if ui.hazard_btn.isChecked():
            active_btn = "hazard"
        elif ui.blinker_left_btn.isChecked():
            active_btn = "left"
        elif ui.blinker_right_btn.isChecked():
            active_btn = "right"

        # Update blink state based on time interval
        if active_btn and now - last_blink_time >= BLINK_INTERVAL:
            blink_state = not blink_state
            last_blink_time = now

        # Set VehicleData blinker states
        data.set_hazard(active_btn == "hazard" and blink_state)
        data.set_left_blinker(active_btn == "left" and blink_state)
        data.set_right_blinker(active_btn == "right" and blink_state)

        # SET-Signals sending to KUKSA
        if kuksa_client:
            try:
                kuksa_client.set_current_values({
                    SET_SIGNALS["highbeam"]: Datapoint(value=data.get_highbeam()),
                    SET_SIGNALS["lowbeam"]: Datapoint(value=data.get_lowbeam()),
                    SET_SIGNALS["standlight"]: Datapoint(value=data.get_standlight()),
                    SET_SIGNALS["hazard"]: Datapoint(value=data.get_hazard()),
                    SET_SIGNALS["left"]: Datapoint(value=data.get_left_blinker()),
                    SET_SIGNALS["right"]: Datapoint(value=data.get_right_blinker()),
                    SET_SIGNALS["interior_light"]: Datapoint(value=data.get_interior_light()),
                })
            except Exception as e:
                print("⚠️ Fehler beim Publishen an KUKSA:", e)

        time.sleep(0.05)  # protect CPU


def gui_thread(data: VehicleData):
    ### GUI Thread ###
    app = QApplication(sys.argv)
    ui = SDV_UI()
    ui.show()
    # Button Klick -> toggelt info_cnt
    ui.information_btn.clicked.connect(lambda: data.toggle_info_cnt())

    def update_ui():
        # Indicators & Lights
        ui.highbeam.setVisible(data.get_highbeam())
        ui.lowbeam.setVisible(data.get_lowbeam())
        ui.stand.setVisible(data.get_standlight())
        ui.interiorlight.setVisible(data.get_interior_light())
        ui.blinker_left.setVisible(data.get_left_blinker() or data.get_hazard())
        ui.blinker_right.setVisible(data.get_right_blinker() or data.get_hazard())
        

        # Doors
        ui.door_both.setVisible(data.get_door_status() == 1)
        ui.door_left.setVisible(data.get_door_status() == 2)
        ui.door_right.setVisible(data.get_door_status() == 3)
                               
        # Speed
        ui.speed.setText(str(int(data.get_speed())))

        # Gear
        gear = int(data.get_gear())

        if gear == 0:
            ui.gear.setText("N")     # Neutral
        elif gear == 126:
            ui.gear.setText("P")     # Park
        elif gear == 127:
            ui.gear.setText("D")     # Drive-Mode
        elif gear > 0:
            ui.gear.setText(f"D{gear}")   # Forward gears
        elif gear < 0:
            ui.gear.setText(f"R{abs(gear)}")  # Reverse gears
        else:
            ui.gear.setText("?")     # Fallback

        # Parksensor
        active = data.get_parksensor_active()  
        level = data.get_parksensor_level()  
        distance = data.get_parksensor_distance()
        ui.update_distance_bar(distance)

        if active and gear < 0: # just when driving in reverse gear
            ui.parksensor_0.setVisible(level == 0)
            ui.parksensor_1.setVisible(level == 1)
            ui.parksensor_2.setVisible(level == 2)
            ui.parksensor_3.setVisible(level == 3)
            if (level == 3):
                ui.distance_bar_bg.show()
                ui.distance_bar_fill.show()
            else: 
                ui.distance_bar_bg.hide()
                ui.distance_bar_fill.hide()
        else:
            ui.parksensor_0.hide()
            ui.parksensor_1.hide()
            ui.parksensor_2.hide()
            ui.parksensor_3.hide()
            ui.distance_bar_bg.hide()
            ui.distance_bar_fill.hide()
      
        # Person Detection

        if data.get_person_detected() and gear >= 0:
            ui.person.show()
            ui.person_distance.show()
            ui.person_distance_cm.show()
            ui.person_distance.setText(str(data.get_person_distance()))
        else:
            ui.person.hide()
            ui.person_distance.hide()
            ui.person_distance_cm.hide()

        # Fuel Range & Level
        if data.get_info_cnt() == False:
            ui.info_label.setText("Odometer:")
            ui.info.setText(str(round(data.get_odometer())))
        elif data.get_info_cnt() == True:
            ui.info_label.setText("Range:")
            ui.info.setText(str(round(data.get_fuel_range())))  
                
        ui.fuel10.setVisible(data.get_fuel_level() > 90)
        ui.fuel9.setVisible(80 < data.get_fuel_level() <= 90)
        ui.fuel8.setVisible(70 < data.get_fuel_level() <= 80)
        ui.fuel7.setVisible(60 < data.get_fuel_level() <= 70)
        ui.fuel6.setVisible(50 < data.get_fuel_level() <= 60)
        ui.fuel5.setVisible(40 < data.get_fuel_level() <= 50)
        ui.fuel4.setVisible(30 < data.get_fuel_level() <= 40)
        ui.fuel3.setVisible(20 < data.get_fuel_level() <= 30)
        ui.fuel2.setVisible(10 < data.get_fuel_level() <= 20)
        ui.fuel1.setVisible(0 < data.get_fuel_level() <= 10)
        ui.fuel0.setVisible(data.get_fuel_level() == 0)



    timer = QTimer()
    timer.timeout.connect(update_ui)
    timer.start(100)

    threading.Thread(target=input_thread, args=(data, ui), daemon=True).start()
    sys.exit(app.exec())


if __name__ == "__main__":
    data = VehicleData()
    gui_thread(data)
