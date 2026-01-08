import sys
from functools import partial
from multiprocessing import Process

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from daemon_notify import daemon_process
from editor import NotificationEditor
from storage import load_notifications, save_notifications

APP_STYLE = """
#central {
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
}

QFrame {
    background-color: rgba(0,0,0,0.4);
    border-radius: 10px;
}
#notif_record {
    color: white;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notify daemon")

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.create_btn = QPushButton("➕ Создать уведомление")
        layout.addWidget(self.create_btn)

        self.list_layout = QVBoxLayout()
        layout.addLayout(self.list_layout)
        layout.addStretch()

        self.setStyleSheet(APP_STYLE)

        self.create_btn.clicked.connect(self.create_notification)

        self.notifications = load_notifications()
        self.render()

    def create_notification(self):
        dialog = NotificationEditor(self)
        if dialog.exec():
            self.notifications.append(dialog.get_data())
            save_notifications(self.notifications)
            self.render()

    def edit_notification(self, i):
        dialog = NotificationEditor(self)
        dialog.set_data(self.notifications[i])
        if dialog.exec():
            self.notifications[i] = dialog.get_data()
            save_notifications(self.notifications)
            self.render()

    def delete_notification(self, i):
        self.notifications.pop(i)
        save_notifications(self.notifications)
        self.render()

    def render(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, n in enumerate(self.notifications):
            card = QFrame()
            l = QHBoxLayout(card)

            label = QLabel(f"{n['description']} - {n['time']} — {', '.join(n['days'])}")
            label.setObjectName("notif_record")
            delete_btn = QPushButton("удалить")
            edit = QPushButton("редактировать")
            edit.clicked.connect(partial(self.edit_notification, i))
            delete_btn.clicked.connect(partial(self.delete_notification, i))

            l.addWidget(label)
            l.addStretch()
            l.addWidget(delete_btn)
            l.addWidget(edit)

            self.list_layout.addWidget(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    process = Process(target=daemon_process)
    process.start()
    app.exec()
