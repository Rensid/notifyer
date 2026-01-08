from functools import partial

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import (QCheckBox, QDialog, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QTimeEdit, QVBoxLayout)

APP_STYLE = """
QDialog {
    background: qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #1e3c72,
        stop:0.5 #000000,
        stop:1 #6a0dad
    );
}

QPushButton {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 8px 14px;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
}

QFrame {
    background-color: rgba(0,0,0,0.4);
    border-radius: 10px;
}
QCheckBox {
    color: white;
}
QLabel {
    color: white;
}
QTextEdit {
    color: white;
}
"""


class NotificationEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новое уведомление")

        layout = QVBoxLayout(self)

        self.time = QTimeEdit()
        self.time.setDisplayFormat("HH:mm")

        self.days = {}
        days_layout = QHBoxLayout()
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            cb = QCheckBox(d)
            self.days[d] = cb
            days_layout.addWidget(cb)

        self.icon_btn = QPushButton("Иконка (опционально)")
        self.sound_btn = QPushButton("Звук (опционально)")

        self.save_btn = QPushButton("Сохранить")
        self.text_notification = QTextEdit()

        layout.addWidget(QLabel("Текст уведомления"))
        layout.addWidget(self.text_notification)
        layout.addWidget(QLabel("Время"))
        layout.addWidget(self.time)
        layout.addLayout(days_layout)
        layout.addWidget(self.icon_btn)
        layout.addWidget(self.sound_btn)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(APP_STYLE)
        self.save_btn.clicked.connect(self.accept)

    def get_data(self):
        return {
            "description": self.text_notification.toPlainText(),
            "time": self.time.time().toString("HH:mm"),
            "days": [d for d, cb in self.days.items() if cb.isChecked()],
            "icon": None,
            "sound": None,
        }

    def set_data(self, data: dict):
        self.text_notification.setPlainText(data.get("description"))
        self.time.setTime(QTime.fromString(data.get("time"), "HH:mm"))
        for d, cb in self.days.items():
            cb.setChecked(d in data.get("days"))
