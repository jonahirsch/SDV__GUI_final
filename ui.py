from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QButtonGroup
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize


class SDV_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDV Dashboard")
        self.setStyleSheet("background-color: #121212;")
        self.setFixedSize(1024, 600)
        #self.setWindowFlags(Qt.FramelessWindowHint) # optional: frameless window

        # Speed
        self.speed = QLabel("0", self)
        self.speed.setFont(QFont("Tahoma", 85))
        self.speed.setStyleSheet("color: white;")
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setGeometry(55, 20, 300, 120)  # fixed size and position

        self.km_h = QLabel("km/h", self)
        self.km_h.setFont(QFont("Tahoma", 25))
        self.km_h.setStyleSheet("color: white;")
        self.km_h.move(300, 96)

        # Gear
        self.gear = QLabel("P", self)
        self.gear.setFont(QFont("Tahoma", 35))
        self.gear.setStyleSheet("color: white;")
        self.gear.setAlignment(Qt.AlignCenter)
        self.gear.setGeometry(50, 180, 300, 60)

        # Fuel range
        self.fuel_range = QLabel("0", self)
        self.fuel_range.setFont(QFont("Tahoma", 35))
        self.fuel_range.setStyleSheet("color: white;")
        self.fuel_range.move(800, 146) # anpassen
        self.fuel_range_km = QLabel("km", self)
        self.fuel_range_km.setFont(QFont("Tahoma", 25))
        self.fuel_range_km.setStyleSheet("color: white;")
        self.fuel_range_km.move(930, 146) #anpassen vielleicht auch tank dann weiter links

        # Person AI distance
        self.person_distance = QLabel("000", self)
        self.person_distance.setFont(QFont("Tahoma", 35))
        self.person_distance.setStyleSheet("color: #fd2d00;")
        self.person_distance.setAlignment(Qt.AlignCenter)
        self.person_distance.setGeometry(215, 428, 100, 50)
        self.person_distance.hide()

        self.person_distance_cm = QLabel("cm", self)
        self.person_distance_cm.setFont(QFont("Tahoma", 25))
        self.person_distance_cm.setStyleSheet("color: #fd2d00;")
        self.person_distance_cm.move(310, 442)
        self.person_distance_cm.hide()

        
        # Buttons
        self.blinker_right_btn = self._make_button(876, 306, "icons/blinker_right_button.JPG")
        self.highbeam_btn = self._make_button(876, 452, "icons/highbeam_button.JPG")
        self.hazard_btn = self._make_button(730, 306, "icons/hazard_button.png")
        self.lowbeam_btn = self._make_button(730, 452, "icons/lowbeam_button.JPG")
        self.blinker_left_btn = self._make_button(584, 306, "icons/blinker_left_button.JPG")
        self.stand_light_btn = self._make_button(584, 452, "icons/stand_button.JPG")

        # blinker lights group
        self.blinker_group = [self.blinker_left_btn, self.blinker_right_btn, self.hazard_btn]

        # blinker lights group exclusivity (manual, allow deactivation)
        def toggle_blinker(button):
            if button.isChecked():
                for b in self.blinker_group: # activate -> button on, disable others
                    if b != button:
                        b.setChecked(False)
            else:
                button.setChecked(False) # deactivate -> button off

        # connect buttons to the toggle function
        for b in self.blinker_group:
            b.clicked.connect(lambda checked, btn=b: toggle_blinker(btn))

        # body lights group
        self.light_group_buttons = [self.stand_light_btn, self.highbeam_btn, self.lowbeam_btn]
        # body lights group exclusivity (manual, allow deactivation)
        def toggle_light(button):
            if button.isChecked():
                for b in self.light_group_buttons: # activate -> button on, disable others
                    if b != button:
                        b.setChecked(False)
            else:
                button.setChecked(False)

        # connect buttons to the toggle function
        for b in self.light_group_buttons:
            b.clicked.connect(lambda checked, btn=b: toggle_light(btn))


        # Images

        # Blinker images
        self.blinker_left = self._make_image(8, 140, "icons/blinker_left.JPG")
        self.blinker_right = self._make_image(247, 140, "icons/blinker_right.JPG")
        
        # Light images
        self.stand = self._make_image(876, 8, "icons/stand.JPG") #prev: 584,8
        self.lowbeam = self._make_image(876, 8, "icons/lowbeam.JPG") #prev: 730,8
        self.highbeam = self._make_image(876, 8, "icons/highbeam.JPG")

        # Türen
        self.door_both = self._make_image(584, 8, "icons/door_both.JPG") #all prev: 730, 146
        self.door_left = self._make_image(584, 8, "icons/door_left.JPG")
        self.door_right = self._make_image(584, 8, "icons/door_right.JPG")

        # Parksensoren
        self.parksensor_0 = self._make_image(8, 380, "icons/parksensor0.jpg")
        self.parksensor_1 = self._make_image(8, 380, "icons/parksensor1.jpg")
        self.parksensor_2 = self._make_image(8, 380, "icons/parksensor2.jpg")
        self.parksensor_3 = self._make_image(8, 380, "icons/parksensor3.jpg")
        

        # Person
        self.person = self._make_image(150, 380, "icons/person.jpg")
        self.person.hide()

        # Tank
        self.fuel10 = self._make_image(730, 146, "icons/fuel10.jpg")
        self.fuel9 = self._make_image(730, 146, "icons/fuel9.jpg")
        self.fuel8 = self._make_image(730, 146, "icons/fuel8.jpg")
        self.fuel7 = self._make_image(730, 146, "icons/fuel7.jpg")
        self.fuel6 = self._make_image(730, 146, "icons/fuel6.jpg")
        self.fuel5 = self._make_image(730, 146, "icons/fuel5.jpg")
        self.fuel4 = self._make_image(730, 146, "icons/fuel4.jpg")
        self.fuel3 = self._make_image(730, 146, "icons/fuel3.jpg")
        self.fuel2 = self._make_image(730, 146, "icons/fuel2.jpg")
        self.fuel1 = self._make_image(730, 146, "icons/fuel1.jpg")
        self.fuel0 = self._make_image(730, 146, "icons/fuel0.jpg")
        self.fuel10.hide()
        self.fuel9.hide()
        self.fuel8.hide()
        self.fuel7.hide()
        self.fuel6.hide()
        self.fuel5.hide()
        self.fuel4.hide()
        self.fuel3.hide()
        self.fuel2.hide()
        self.fuel1.hide()
        self.fuel0.hide()
                                       

    def _make_button(self, x, y, icon_path):
        btn = QPushButton(self)
        btn.setGeometry(x, y, 140, 140)
        btn.setCheckable(True)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(120, 120))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1A1A1A;
                border: 2px solid #222;
                border-radius: 10px;
            }
            QPushButton:checked {
                border: 3px solid #00FFC8;
                background-color: #1E1E1E;
            }
        """)
        return btn

    def _make_image(self, x, y, img_path):
        label = QLabel(self)
        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.move(x, y)
        return label
