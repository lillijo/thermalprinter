from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

def on_button_clicked():
    button.setEnabled(False)
    cfg = picam2.create_still_configuration(raw={})
    picam2.switch_mode_and_capture_file(cfg, "test.dng", name="raw", wait=False, signal_function=qpicamera2.signal_done)

def capture_done():
    button.setEnabled(True)

app = QApplication([])
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration({"size": (800, 600)}))
qpicamera2 = QGlPicamera2(picam2, width=800, height=600, keep_ar=False)
button = QPushButton("Click here to capture DNG file")
window = QWidget()
qpicamera2.done_signal.connect(capture_done)
button.clicked.connect(on_button_clicked)

layout_v = QVBoxLayout()
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button)
window.setWindowTitle("Raw Capture")
window.resize(800, 600)
window.setLayout(layout_v)

picam2.start()
window.show()
app.exec()
