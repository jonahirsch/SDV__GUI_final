import os
from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize

# ============================================================
# Absolute path handling (VERY IMPORTANT)
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "icons")


class SDV_UI(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------- WINDOW ----------------
        self.setWindowTitle("SDV UI")
        self.setStyleSheet("background-color: #121212;")
        self.setFixedSize(1024, 600)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        # ---------------- SPEED ----------------
        self.speed = QLabel("0", self)
        self.speed.setFont(QFont("Tahoma", 85))
        self.speed.setStyleSheet("color: white;")
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setGeometry(55, 20, 300, 120)

        self.km_h = QLabel("km/h", self)
        self.km_h.setFont(QFont("Tahoma", 25))
        self.km_h.setStyleSheet("color: white;")
        self.km_h.move(300, 96)

        # ---------------- GEAR ----------------
        self.gear = QLabel("P", self)
        self.gear.setFont(QFont("Tahoma", 35))
        self.gear.setStyleSheet("color: white;")
        self.gear.setAlignment(Qt.AlignCenter)
        self.gear.setGeometry(50, 180, 300, 60)

        # ---------------- INFORMATION ----------------
        self.info_label = QLabel("Information:", self)
        self.info_label.setFont(QFont("Tahoma", 25))
        self.info_label.setStyleSheet("color: white;")
        self.info_label.move(660, 161)

        self.info = QLabel("0000000", self)
        self.info.setFont(QFont("Tahoma", 25))
        self.info.setStyleSheet("color: white;")
        self.info.move(680, 226)

        self.info_km = QLabel("km", self)
        self.info_km.setFont(QFont("Tahoma", 15))
        self.info_km.setStyleSheet("color: white;")
        self.info_km.move(810, 241)

        # ---------------- PERSON DISTANCE ----------------
        self.person_distance = QLabel("0000", self)
        self.person_distance.setFont(QFont("Tahoma", 25))
        self.person_distance.setStyleSheet("color: #fd2d00;")
        self.person_distance.move(240, 530)
        self.person_distance.hide()

        self.person_distance_cm = QLabel("cm", self)
        self.person_distance_cm.setFont(QFont("Tahoma", 15))
        self.person_distance_cm.setStyleSheet("color: #fd2d00;")
        self.person_distance_cm.move(315, 545)
        self.person_distance_cm.hide()

        # ---------------- BUTTONS ----------------
        self.blinker_right_btn = self._make_button(876, 306, "blinker_right_button.JPG")
        self.highbeam_btn = self._make_button(876, 452, "highbeam_button.JPG")
        self.hazard_btn = self._make_button(730, 306, "hazard_button.png")
        self.lowbeam_btn = self._make_button(730, 452, "lowbeam_button.JPG")
        self.blinker_left_btn = self._make_button(584, 306, "blinker_left_button.JPG")
        self.stand_light_btn = self._make_button(584, 452, "stand_button.JPG")
        self.interiorlight_btn = self._make_button(438, 452, "interiorlight_button.JPG")
        self.information_btn = self._make_button_noswitch(438, 306, "information_btn.jpg")

        # ---------------- GROUP LOGIC ----------------
        # ---------------- GROUP LOGIC (XOR – FIXED) ----------------
        self.blinker_group = [
            self.blinker_left_btn,
            self.blinker_right_btn,
            self.hazard_btn,
        ]

        self.light_group_buttons = [
            self.stand_light_btn,
            self.highbeam_btn,
            self.lowbeam_btn,
        ]

        def xor_toggle(active_btn, group):
            if not active_btn.isChecked():
                return

            for btn in group:
                if btn is not active_btn:
                    btn.blockSignals(True)
                    btn.setChecked(False)
                    btn.blockSignals(False)

        for btn in self.blinker_group:
            btn.clicked.connect(lambda _, b=btn: xor_toggle(b, self.blinker_group))

        for btn in self.light_group_buttons:
            btn.clicked.connect(lambda _, b=btn: xor_toggle(b, self.light_group_buttons))


        # ---------------- IMAGES ----------------
        self.blinker_left = self._make_image(8, 140, "blinker_left.JPG")
        self.blinker_right = self._make_image(247, 140, "blinker_right.JPG")

        self.stand = self._make_image(876, 8, "stand.JPG")
        self.lowbeam = self._make_image(876, 8, "lowbeam.JPG")
        self.highbeam = self._make_image(876, 8, "highbeam.JPG")
        self.interiorlight = self._make_image(730, 8, "interiorlight.JPG")

        self.door_both = self._make_image(584, 8, "door_both.JPG")
        self.door_left = self._make_image(584, 8, "door_left.JPG")
        self.door_right = self._make_image(584, 8, "door_right.JPG")

        self.parksensor_0 = self._make_image_extend(8, 330, "parksensor0.jpg")
        self.parksensor_1 = self._make_image_extend(8, 330, "parksensor1.jpg")
        self.parksensor_2 = self._make_image_extend(8, 330, "parksensor2.jpg")
        self.parksensor_3 = self._make_image_extend(8, 330, "parksensor3.jpg")

        # ---------------- DISTANCE BAR ----------------
        self.distance_bar_bg = QLabel(self)
        self.distance_bar_bg.setGeometry(8, 530, 240, 20)
        self.distance_bar_bg.setStyleSheet(
            "background-color: #1A1A1A; border-radius: 5px;"
        )

        self.distance_bar_fill = QLabel(self)
        self.distance_bar_fill.setGeometry(8, 530, 0, 20)
        self.distance_bar_fill.setStyleSheet(
            "background-color: #fd2d00; border-radius: 5px;"
        )

        # ---------------- PERSON ----------------
        self.person = self._make_image_extend(150, 380, "person.jpg")
        self.person.hide()

        # ---------------- FUEL (backward compatible) ----------------
        self.fuel0 = self._make_image(520, 156, "fuel0.jpg")
        self.fuel1 = self._make_image(520, 156, "fuel1.jpg")
        self.fuel2 = self._make_image(520, 156, "fuel2.jpg")
        self.fuel3 = self._make_image(520, 156, "fuel3.jpg")
        self.fuel4 = self._make_image(520, 156, "fuel4.jpg")
        self.fuel5 = self._make_image(520, 156, "fuel5.jpg")
        self.fuel6 = self._make_image(520, 156, "fuel6.jpg")
        self.fuel7 = self._make_image(520, 156, "fuel7.jpg")
        self.fuel8 = self._make_image(520, 156, "fuel8.jpg")
        self.fuel9 = self._make_image(520, 156, "fuel9.jpg")
        self.fuel10 = self._make_image(520, 156, "fuel10.jpg")

        self.fuel_imgs = [
            self.fuel0, self.fuel1, self.fuel2, self.fuel3, self.fuel4,
            self.fuel5, self.fuel6, self.fuel7, self.fuel8, self.fuel9,
            self.fuel10,
        ]

        for img in self.fuel_imgs:
            img.hide()

    # ============================================================
    # Helper methods
    # ============================================================
    def _icon(self, filename):
        path = os.path.join(ICON_DIR, filename)
        if not os.path.exists(path):
            print(f"[WARN] Missing icon: {path}")
        return path

    def _make_button(self, x, y, icon_name):
        btn = QPushButton(self)
        btn.setGeometry(x, y, 140, 140)
        btn.setCheckable(True)
        btn.setIcon(QIcon(self._icon(icon_name)))
        btn.setIconSize(QSize(120, 120))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            """
            QPushButton { background-color: #1A1A1A; border: 2px solid #222; border-radius: 10px; }
            QPushButton:checked { border: 3px solid #00FFC8; background-color: #1E1E1E; }
            """
        )
        return btn

    def _make_button_noswitch(self, x, y, icon_name):
        btn = QPushButton(self)
        btn.setGeometry(x, y, 140, 140)
        btn.setCheckable(False)
        btn.setIcon(QIcon(self._icon(icon_name)))
        btn.setIconSize(QSize(120, 120))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            """
            QPushButton { background-color: #1A1A1A; border: 2px solid #222; border-radius: 10px; }
            QPushButton:pressed { border: 3px solid #00FFC8; background-color: #1E1E1E; }
            """
        )
        return btn

    def _make_image(self, x, y, img_name):
        label = QLabel(self)
        pixmap = QPixmap(self._icon(img_name))
        if pixmap.isNull():
            print(f"[WARN] Image not loaded: {img_name}")
        label.setPixmap(
            pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        label.move(x, y)
        return label

    def _make_image_extend(self, x, y, img_name):
        label = QLabel(self)
        pixmap = QPixmap(self._icon(img_name))
        if pixmap.isNull():
            print(f"[WARN] Image not loaded: {img_name}")
        label.setPixmap(
            pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        label.move(x, y)
        return label

    def update_distance_bar(self, cm):
        cm = max(0, min(50, cm))
        color = "#fd2d00" if cm < 30 else "#ce7927" if cm < 40 else "#9fc54e"
        self.distance_bar_fill.setStyleSheet(
            f"background-color: {color}; border-radius: 5px;"
        )
        self.distance_bar_fill.setGeometry(8, 530, int(240 * cm / 50), 20)
