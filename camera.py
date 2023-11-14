"""PyQt5 Multimedia Camera Example"""

import os
import sys
from PyQt5.QtCore import QDate, QTime, QDir, QStandardPaths, Qt, QUrl, QTimer, QSize
from PyQt5.QtGui import QGuiApplication, QDesktopServices, QIcon
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    QLabel,
    QMainWindow,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QTabBar,
)
from PyQt5.QtMultimedia import (
    QCamera,
    QCameraInfo,
    QCameraImageCapture,
)
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from keyboard import DescriptionDialog
from drawing import Drawing


class ImageView(QWidget):
    def __init__(self, previewImage, fileName, description):
        super().__init__()

        self._file_name = fileName
        self.printing_status = ""
        main_layout = QVBoxLayout(self)
        self._image_label = QLabel()
        self._image_label.setPixmap(QPixmap.fromImage(previewImage))
        main_layout.addWidget(self._image_label)
        self._file_name_label = QLabel(QDir.toNativeSeparators(fileName))
        self.description = QLabel(description)

        main_layout.addWidget(self._file_name_label)
        main_layout.addWidget(self.description)
        main_layout.setSpacing(0)
        main_layout.addStretch(10)

    def copy(self):
        QGuiApplication.clipboard().setText(self._file_name_label.text())

    def launch(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self._file_name))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._capture_session = None
        self._camera = None
        self._camera_info = None
        self._image_capture = None
        self.counter = 3
        self._file_name = ""
        date_string = QDate.currentDate().toString("dd-MM-yyyy")
        self.description = f"Bild {date_string}"
        self._camera_viewfinder = QCameraViewfinder()
        available_cameras = QCameraInfo.availableCameras()
        if available_cameras:
            self._camera_info = available_cameras[0]
            self._camera = QCamera(self._camera_info)
            self._camera.setCaptureMode(QCamera.CaptureMode.CaptureStillImage)
            self._camera.errorOccurred.connect(self._camera_error)
            self._camera.setViewfinder(self._camera_viewfinder)
            self._image_capture = QCameraImageCapture(self._camera)
            self._image_capture.imageCaptured.connect(self.image_captured)
            self._image_capture.imageSaved.connect(self.image_saved)
            self._image_capture.error.connect(self._capture_error)

        self._current_preview = QImage()

        tool_bar = QToolBar()
        tool_bar.setOrientation(Qt.Orientation.Vertical)
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)
        tool_bar.setIconSize(QSize(50, 50))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tool_bar)

        shutter_icon = QIcon(os.path.join(os.path.dirname(__file__), "trigger.png"))
        self._take_picture_action = QAction(
            shutter_icon,
            "&Take Picture",
            self,
            shortcut="Ctrl+T",
            triggered=self.take_picture,
        )
        self._take_picture_action.setToolTip("Take Picture")
        tool_bar.addAction(self._take_picture_action)

        self.button_edit = QAction(QIcon("write.png"), "D", self)
        self.button_edit.triggered.connect(self.onEditDescription)
        self.button_edit.setToolTip("Write Image Heading")
        tool_bar.addAction(self.button_edit)

        self.button_draw = QAction(QIcon("draw.png"), "D", self)
        self.button_draw.triggered.connect(self.onDrawImage)
        self.button_draw.setToolTip("Draw Onto Image")
        tool_bar.addAction(self.button_draw)

        self.button_print = QAction(QIcon("printer.png"), "P", self)
        self.button_print.triggered.connect(self.onPrintPhoto)
        self.button_print.setToolTip("Print Image")
        tool_bar.addAction(self.button_print)

        self.button_reset = QAction(QIcon("reset.png"), "P", self)
        self.button_reset.triggered.connect(self.onAbandonPhoto)
        self.button_reset.setToolTip("reset to camera")
        tool_bar.addAction(self.button_reset)

        self.finish = QAction(QIcon("close.png"), "Q", self)
        self.finish.triggered.connect(self.closeEvent)
        tool_bar.addAction(self.finish)

        self._tab_widget = QTabWidget(self, tabsClosable=True)
        self._tab_widget.setStyleSheet(
            "QTabWidget::pane { margin: 0px; border: none; padding: 0px; top: -40px;}"
        )
        self.setCentralWidget(self._tab_widget)

        self._tab_widget.addTab(self._camera_viewfinder, "Take Image")
        self._tab_widget.tabBar().setTabButton(
            0, QTabBar.ButtonPosition.RightSide, None
        )
        self._tab_widget.tabCloseRequested.connect(self._tab_widget.tabBar().removeTab)

        if self._camera and self._camera.error() != QCamera.Error:
            name = self._camera_info.description()
            self.setWindowTitle(f"Thermal Printer ({name})")
            self.show_status_message(f"Starting: '{name}'")
            # self._capture_session.setVideoOutput(self._camera_viewfinder)
            self._take_picture_action.setEnabled(
                self._image_capture.isReadyForCapture()
            )
            self._image_capture.readyForCaptureChanged.connect(
                self._take_picture_action.setEnabled
            )
            self._camera.start()
        else:
            self.setWindowTitle("Thermal Printer")
            self._take_picture_action.setEnabled(False)
            self.show_status_message("Camera unavailable")

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)

    def closeEvent(self, event):
        if self._camera and self._camera.status() == QCamera.Status.ActiveStatus:
            self._camera.stop()
        self.close()

    def next_image_file_name(self):
        pictures_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DesktopLocation
        )
        datestr = QDate.currentDate().toString("dd_MM_yyyy")
        timestr = QTime().currentTime().toString("hh_mm")
        picname = f"{datestr}_{timestr}_image"
        self._file_name = f"{pictures_location}/{picname}.jpg"
        return self._file_name

    def countdown(self):
        if self.counter > 0:
            self.show_status_message(str(self.counter))
            self.counter -= 1
            QTimer.singleShot(500, self.countdown)
        elif self.counter == 0:
            self.show_status_message("GO!")
            self.counter -= 1
            QTimer.singleShot(500, self.countdown)
        else:
            self._current_preview = QImage()
            self._image_capture.capture(self.next_image_file_name())
            self.show_status_message("")
            self.counter = 3

    def take_picture(self):
        self.countdown()

    def image_captured(self, id, previewImage):
        self._current_preview = previewImage

    def image_saved(self, id, fileName):
        index = self._tab_widget.count()
        image_view = ImageView(self._current_preview, fileName, self.description)
        self._tab_widget.addTab(image_view, f"Capture #{index}")
        self._tab_widget.setCurrentIndex(index)

    def _capture_error(self, id, error, error_string):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    def _camera_error(self, error, error_string=None):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    def print_description_func(self):
        loc = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DesktopLocation
        )
        description_loc = f"{loc}/description.txt"
        if os.path.isfile(description_loc):
            os.system(f"cat {description_loc} | lp")
            self.show_status_message("Printing Description ...")
        else:
            self.show_status_message("Description not found")

    def print_image_func(self):
        fn = self._file_name
        if os.path.isfile(fn):
            os.system(f"lp -o landscape -o fit-to-page {fn}")
            self.show_status_message(f"Printing Image {fn} ...")
        else:
            self.show_status_message("Image not found")
        QTimer.singleShot(1000, self.print_description_func)

    def onPrintPhoto(self):
        self.show_status_message("printing...")
        QTimer.singleShot(1000, self.print_image_func)

    def onAbandonPhoto(self):
        if self._tab_widget.count() > 1:
            self._tab_widget.tabBar().removeTab(1)
            print("back to camera!")

    def onDrawImage(self):
        if self._file_name == "":
            fn = self.next_image_file_name()
            img = QImage(self.size(), QImage.Format.Format_Grayscale8)
            img.fill(Qt.white)
            drawing_view = Drawing(fn, img)
            self.show_status_message("Draw new Image")
        else:
            drawing_view = Drawing(self._file_name, self._current_preview)
            self.show_status_message("Draw on Image")
        #self._tab_widget.addTab(drawing_view, "Draw on Image")
        if drawing_view.exec():
            print("Success!")
        else:
            print("Cancel!")

    def onEditDescription(self):
        ddialog = DescriptionDialog(self.description)
        if ddialog.exec():
            print("Success!")
        else:
            print("Cancel!")
        print("edit description")


def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width(), available_geometry.height() - 40)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
