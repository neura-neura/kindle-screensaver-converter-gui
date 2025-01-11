import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QSpinBox, QPushButton, QFileDialog, QScrollArea, 
    QFrame, QProgressBar, QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QFont, QIcon
from PIL import Image, ImageEnhance
import qdarktheme

class ImageProcessor(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, params, input_folder):
        super().__init__()
        self.params = params
        self.input_folder = input_folder

    def enhance_contrast_grayscale(self, image):
        image = image.convert("L")
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)

    def adjust_bit_depth(self, image, bit_depth):
        if bit_depth == 8:
            return image  # 8-bit is the default value for grayscale images.
        
        # Calculate number of gray levels based on bit depth
        levels = 2 ** bit_depth - 1
        
        # Convert to array for pixel manipulation
        import numpy as np
        img_array = np.array(image)
        
        # Normalize and adjust to new bit range
        normalized = img_array / 255.0  # Normalize to range 0-1
        adjusted = np.round(normalized * levels) * (255 / levels)  # Adjust to new range and scale back to 8 bits
        
        # Convert back to PIL image
        return Image.fromarray(adjusted.astype(np.uint8))

    def run(self):
        output_folder = "converted_screensavers"
        os.makedirs(output_folder, exist_ok=True)
        
        images = [f for f in os.listdir(self.input_folder) 
                 if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        
        for idx, image_name in enumerate(images):
            image_path = os.path.join(self.input_folder, image_name)
            with Image.open(image_path) as img:
                # Convert and resize
                img = img.convert("RGB")
                scale_factor = max(self.params['width'] / img.width, 
                                 self.params['height'] / img.height)
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # Crop
                left = (img.width - self.params['width']) // 2
                top = (img.height - self.params['height']) // 2
                right = left + self.params['width']
                bottom = top + self.params['height']
                img = img.crop((left, top, right, bottom))
                
                # Convert to grayscale and improve contrast
                img = self.enhance_contrast_grayscale(img)
                
                # Adjust bit depth
                img = self.adjust_bit_depth(img, self.params['bit_depth'])
                
                # Save
                output_name = f"bg_ss{str(idx + 1).zfill(2)}.png"
                output_path = os.path.join(output_folder, output_name)
                img.save(output_path, "PNG", 
                        dpi=(self.params['dpi_x'], self.params['dpi_y']))
            
            self.progress.emit(int((idx + 1) / len(images) * 100))
        
        self.finished.emit()

class ImageThumbnail(QFrame):
    def __init__(self, image_path):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        layout = QVBoxLayout()
        
        # Image
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Filename
        filename_label = QLabel(os.path.basename(image_path))
        filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filename_label.setWordWrap(True)
        
        layout.addWidget(image_label)
        layout.addWidget(filename_label)
        self.setLayout(layout)

class KindleConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.input_folder = "PUT YOUR IMAGES HERE"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kindle Screensaver Converter')
        self.setMinimumSize(800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Title
        title_label = QLabel("Kindle Screensaver Converter")
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Parameters section
        params_frame = QFrame()
        params_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        params_layout = QGridLayout(params_frame)

        # Parameter input fields
        self.params = {}
        param_configs = {
            'height': ('Target Height (pixels):', 800, 1, 2000),
            'width': ('Target Width (pixels):', 600, 1, 2000),
            'dpi_x': ('Horizontal DPI:', 96, 1, 600),
            'dpi_y': ('Vertical DPI:', 96, 1, 600),
            'bit_depth': ('Bit Depth:', 8, 1, 32)
        }

        for i, (key, (label, default, min_val, max_val)) in enumerate(param_configs.items()):
            params_layout.addWidget(QLabel(label), i, 0)
            spinbox = QSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setValue(default)
            self.params[key] = spinbox
            params_layout.addWidget(spinbox, i, 1)

        layout.addWidget(params_frame)

        # Image preview section
        self.preview_area = QScrollArea()
        self.preview_widget = QWidget()
        self.preview_layout = QGridLayout(self.preview_widget)
        self.preview_area.setWidget(self.preview_widget)
        self.preview_area.setWidgetResizable(True)
        layout.addWidget(self.preview_area)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.select_folder_btn = QPushButton('Select Input Folder')
        self.select_folder_btn.clicked.connect(self.select_input_folder)
        
        self.convert_btn = QPushButton('Convert Images')
        self.convert_btn.clicked.connect(self.start_conversion)
        
        button_layout.addWidget(self.select_folder_btn)
        button_layout.addWidget(self.convert_btn)
        layout.addLayout(button_layout)

        # Credits button
        self.made_by_neura_btn = QPushButton('Made by neura')
        self.made_by_neura_btn.clicked.connect(lambda: os.system('start https://github.com/neura-neura/kindle-screensaver-converter-gui'))
        layout.addWidget(self.made_by_neura_btn)

        # Load initial images
        self.load_image_previews()

    def load_image_previews(self):
        # Clear existing previews
        for i in reversed(range(self.preview_layout.count())): 
            self.preview_layout.itemAt(i).widget().setParent(None)

        if os.path.exists(self.input_folder):
            images = [f for f in os.listdir(self.input_folder) 
                     if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            
            row = 0
            col = 0
            for image in images:
                image_path = os.path.join(self.input_folder, image)
                thumbnail = ImageThumbnail(image_path)
                self.preview_layout.addWidget(thumbnail, row, col)
                col += 1
                if col > 3:  # 4 thumbnails per row
                    col = 0
                    row += 1

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.load_image_previews()

    def start_conversion(self):
        params = {key: spinbox.value() for key, spinbox in self.params.items()}
        
        self.processor = ImageProcessor(params, self.input_folder)
        self.processor.progress.connect(self.update_progress)
        self.processor.finished.connect(self.conversion_finished)
        
        self.progress_bar.setVisible(True)
        self.convert_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        
        self.processor.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", 
            "Images have been converted successfully!\nCheck the 'converted_screensavers' folder.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Aplicar el tema oscuro usando la API correcta
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = KindleConverterGUI()
    window.show()
    sys.exit(app.exec())