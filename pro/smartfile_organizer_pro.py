APP_VERSION = "1.0.0"
APP_NAME = "Smart File Organizer"
APP_AUTHOR = "The DevOps Rite"
APP_WEBSITE = "https://github.com/TheDevOpsRite"

from PySide6.QtWidgets import QSplashScreen
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
import platform
import sys
import os
import shutil
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox
)
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QMenuBar, QMenu, QDialog, QVBoxLayout, QLineEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import json
import urllib.request
import urllib.error


LICENSE_API_URL = "http://localhost:5000/api/license/verify"  # TODO: set to your backend endpoint, e.g. "https://example.com/api/license/verify"
LICENSE_API_TIMEOUT_SEC = 8


def verify_license_key_online(license_key: str) -> bool:
    if not LICENSE_API_URL or not LICENSE_API_URL.strip():
        raise RuntimeError("LICENSE_API_URL is not configured")

    payload = json.dumps({"licenseKey": license_key}).encode("utf-8")
    request = urllib.request.Request(
        LICENSE_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=LICENSE_API_TIMEOUT_SEC) as response:
        body = response.read().decode("utf-8", errors="replace")

    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"License API returned non-JSON response: {e}")

    valid = data.get("valid")
    if isinstance(valid, bool):
        return valid

    raise RuntimeError('License API response must include boolean field "valid"')


class LicenseKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("License Key")
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QVBoxLayout()
        title = QLabel("Enter your license key to continue")
        title.setAlignment(Qt.AlignCenter)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("License key")
        self.key_input.returnPressed.connect(self._submit)

        self.get_license_label = QLabel(
            'Get the License key <a href="https://devopsrite.vercel.app/smartfileorganizer.html"><b>here</b></a> for free'
        )
        self.get_license_label.setAlignment(Qt.AlignCenter)
        self.get_license_label.setOpenExternalLinks(True)
        self.get_license_label.setTextFormat(Qt.RichText)
        self.get_license_label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self._submit)

        layout.addWidget(title)
        layout.addWidget(self.key_input)
        layout.addWidget(self.get_license_label)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def _submit(self):
        entered = (self.key_input.text() or "").strip()
        if not entered:
            QMessageBox.warning(self, "Missing Key", "Please enter a license key.")
            return

        self.submit_button.setEnabled(False)
        self.key_input.setEnabled(False)
        try:
            is_valid = verify_license_key_online(entered)
        except urllib.error.HTTPError as e:
            QMessageBox.critical(self, "Verification Failed", f"License API error: HTTP {e.code}")
            return
        except urllib.error.URLError as e:
            QMessageBox.critical(self, "Verification Failed", f"Could not reach license server: {e.reason}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Verification Failed", str(e))
            return
        finally:
            self.submit_button.setEnabled(True)
            self.key_input.setEnabled(True)

        if is_valid:
            self.accept()
        else:
            QMessageBox.critical(self, "Invalid Key", "License key is invalid.")
            self.key_input.clear()
            self.key_input.setFocus()


def require_valid_license(parent=None) -> bool:
    dialog = LicenseKeyDialog(parent=parent)
    return dialog.exec() == QDialog.Accepted


# ================= FILE CATEGORIES =================
file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Text": [".txt", ".md"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Executables": [".exe", ".msi"],
    "Logs": [".log"]
}


# ============ DUPLICATE HANDLING ===================
def get_unique_filename(destination_path):
    base, extension = os.path.splitext(destination_path)
    counter = 1

    while os.path.exists(destination_path):
        destination_path = f"{base}_{counter}{extension}"
        counter += 1

    return destination_path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)        
        
    

# ================= MAIN WINDOW =====================
class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION} - {APP_AUTHOR}")
        self.setMinimumSize(600, 250)

        self.folder_path = ""

        self.init_ui()
        self.apply_styles()
    
    # about section 
    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About")

        layout = QVBoxLayout()

        about_text = QLabel(
            f"""
            <h2>{APP_NAME}</h2>
            <p><b>Version:</b> {APP_VERSION}</p>
            <p><b>Developer:</b> {APP_AUTHOR}</p>
            <p>A professional file organization desktop tool.</p>
            <p>Organize files automatically into structured categories.</p>
            
            <p>Click <a href="{APP_WEBSITE}">here </a>to learn more</p>
            <p>Provide your valueable feedback <a href="https://devopsrite.vercel.app/#contact">here</a></p> 
            """
        )

        about_text.setOpenExternalLinks(True)
        about_text.setAlignment(Qt.AlignCenter)

        layout.addWidget(about_text)
        about_dialog.setLayout(layout)
        about_dialog.resize(400, 250)
        about_dialog.exec()
    
    # section end     

    def open_folder(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Error", "No folder selected.")
            return
        try:
            if platform.system() == "Windows":
                os.startfile(self.folder_path)
            elif platform.system() == "Darwin": #  macOS
                os.system(f"open '{self.folder_path}'") 
            else: # Linux and others
                os.system(f"xdg-open '{self.folder_path}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open folder: {str(e)}")      
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Menu bar 
        menu_bar = QMenuBar(self)

        help_menu = QMenu("Help", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)

        help_menu.addAction(about_action)
        menu_bar.addMenu(help_menu)

        main_layout.setMenuBar(menu_bar)
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)

        original_pixmap = QPixmap(resource_path("app.png"))

        # Resize
        size = 120  # Adjust size here
        scaled_pixmap = original_pixmap.scaled(
            size, size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Create rounded pixmap
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        radius = 25  # 👈 Control roundness here
        path.addRoundedRect(QRectF(0, 0, size, size), radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        self.logo_label.setPixmap(rounded)
        main_layout.addWidget(self.logo_label)


        # Title
        title = QLabel("Smart File Organizer")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")
        main_layout.addWidget(title)

        # Folder Selection Row
        folder_layout = QHBoxLayout()

        self.folder_label = QLabel("No folder selected")
        self.folder_label.setObjectName("folderLabel")

        browse_button = QPushButton("Browse Folder")
        browse_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(browse_button)

        main_layout.addLayout(folder_layout)

        # Buttons Layout (Side by Side)
        button_layout = QHBoxLayout()

        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)

        self.open_button = QPushButton("Open Organized Folder")
        self.open_button.setObjectName("openButton")
        self.open_button.clicked.connect(self.open_folder)

        button_layout.addWidget(self.organize_button)
        button_layout.addWidget(self.open_button)
        

        main_layout.addLayout(button_layout)
        # Output Console
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        main_layout.addWidget(self.output_box)

        # Footer
        footer = QLabel("The DevOps Rite © All Rights Reserved")
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("footer")
        main_layout.addWidget(footer)
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(version_label)

        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Arial;
                font-size: 14px;
            }

            #title {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton {
                background-color: #4CAF50;
                border: none;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {                
                background-color: #45a049;
            }
            QpushButton#openButton{
                background-color: #2196F3;
            }

            QTextEdit {
                background-color: #2b2b3c;
                border-radius: 8px;
                padding: 10px;
            }

            #footer {
                color: #aaaaaa;
                font-size: 11px;
                padding-top: 10px;
            }
        """)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.folder_label.setText(folder)
    
    def organize_files(self):
        if not self.folder_path:            
            QMessageBox.warning(self, "Error", "Please select a folder first.")
            return
        self.output_box.append("\nStarting File Organization...\n")

        try:
            files = os.listdir(self.folder_path)
        except PermissionError:
            self.output_box.append("❌ Permission denied: Cannot access this folder.\n")
            return
        except Exception as e:
            self.output_box.append(f"❌ Error accessing folder: {str(e)}\n")
            return

        for filename in files:
            file_path = os.path.join(self.folder_path, filename)

            if os.path.isdir(file_path):
                continue
    
            if filename.endswith(".log"):
                continue

            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            moved = False

            for category, extensions in file_categories.items():
                if extension in extensions:
                    category_folder = os.path.join(self.folder_path, category)

                    try:
                        if not os.path.exists(category_folder):
                            os.makedirs(category_folder)

                        destination = os.path.join(category_folder, filename)
                        destination = get_unique_filename(destination)

                        shutil.move(file_path, destination)

                        self.output_box.append(f"Moved: {filename} → {category}")
                    except PermissionError:
                        self.output_box.append(f"⚠ Permission denied: {filename}")
                    except Exception as e:
                        self.output_box.append(f"⚠ Error moving {filename}: {str(e)}")

                    moved = True
                    break

            if not moved:
                others_folder = os.path.join(self.folder_path, "Others")

                try:
                    if not os.path.exists(others_folder):
                        os.makedirs(others_folder)

                    destination = os.path.join(others_folder, filename)
                    destination = get_unique_filename(destination)

                    shutil.move(file_path, destination)

                    self.output_box.append(f"Moved: {filename} → Others")
                except PermissionError:
                    self.output_box.append(f"⚠ Permission denied: {filename}")
                except Exception as e:
                    self.output_box.append(f"⚠ Error moving {filename}: {str(e)}")

        self.output_box.append("\nFile Organization Completed Successfully!\n")
# ================= RUN APP =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and scale logo
    original_pixmap = QPixmap(resource_path("app.png"))

    splash_size = 250  # 👈 control splash size here
    scaled_pixmap = original_pixmap.scaled(
        splash_size,
        splash_size,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
    rounded_pixmap = QPixmap(splash_size, splash_size)
    rounded_pixmap.fill(Qt.transparent)
    painter = QPainter(rounded_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    radius = 40  # 👈 control roundness her
    path.addRoundedRect(0, 0, splash_size, splash_size, radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, scaled_pixmap)
    painter.end()

    splash = QSplashScreen(rounded_pixmap)
    splash.setMask(rounded_pixmap.mask())
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.show()

    # Keep global reference
    app.processEvents()
    main_window = None

    def start_main_window():
        global main_window
        splash.hide()
        if not require_valid_license(parent=splash):
            app.quit()
            return

        main_window = FileOrganizerApp()
        main_window.show()
        splash.finish(main_window)

    QTimer.singleShot(3000, start_main_window)  # 2.5 seconds

    sys.exit(app.exec())