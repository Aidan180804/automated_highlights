import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QProgressBar, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal
import yt_dlp

# ------------------------------
# Worker thread for downloading
# ------------------------------
class DownloadThread(QThread):
    progress = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url, output_folder, file_name, download_type):
        super().__init__()
        self.url = url
        self.output_folder = output_folder
        self.file_name = file_name
        self.download_type = download_type

    def run(self):
        try:
            if self.download_type in ["MP4", "Both"]:
                video_path = os.path.join(self.output_folder, self.file_name + "_video.%(ext)s")
                opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'outtmpl': video_path,
                    'merge_output_format': 'mp4',
                    'progress_hooks': [self.hook]
                }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([self.url])

            if self.download_type in ["MP3", "Both"]:
                audio_path = os.path.join(self.output_folder, self.file_name + "_audio.%(ext)s")
                opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'progress_hooks': [self.hook]
                }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([self.url])

            self.finished.emit("Download finished!")

        except Exception as e:
            self.error.emit(str(e))

    def hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%')
            self.progress.emit(f"{d.get('filename','')}  {percent}")
        elif d['status'] == 'finished':
            self.progress.emit(f"Finished downloading: {d.get('filename','')}")


# ------------------------------
# Main Window
# ------------------------------
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setFixedSize(500, 350)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        layout.addWidget(QLabel("Output File Name:"))
        self.file_input = QLineEdit()
        layout.addWidget(self.file_input)

        layout.addWidget(QLabel("Output Folder:"))
        folder_layout = QVBoxLayout()
        self.folder_input = QLineEdit()
        folder_button = QPushButton("Browse...")
        folder_button.clicked.connect(self.choose_folder)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(folder_button)
        layout.addLayout(folder_layout)

        layout.addWidget(QLabel("Download Type:"))
        self.type_select = QComboBox()
        self.type_select.addItems(["MP4", "MP3", "Both"])
        layout.addWidget(self.type_select)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        download_button = QPushButton("Download")
        download_button.clicked.connect(self.start_download)
        layout.addWidget(download_button)

        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        url = self.url_input.text().strip()
        file_name = self.file_input.text().strip()
        folder = self.folder_input.text().strip()
        download_type = self.type_select.currentText()

        if not url or not file_name or not folder:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        self.thread = DownloadThread(url, folder, file_name, download_type)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()
        self.status_label.setText("Status: Downloading...")

    def update_progress(self, text):
        self.status_label.setText(text)

    def download_finished(self, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Done", message)

    def download_error(self, message):
        self.status_label.setText("Error!")
        QMessageBox.critical(self, "Error", message)


# ------------------------------
# Run app
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

