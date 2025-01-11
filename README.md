<div align="center">
  <img src="./assets/icon.ico" alt="Kindle Screensaver Converter GUI icon" width="256">
</div>

<h1 align="center">Kindle Screensaver Converter GUI</h1>

<div align="center">
  This project provides a graphical user interface (GUI) for converting images into Kindle-compatible screensavers, simplifying the process by leveraging the core functionality of the <a href=https://github.com/neura-neura/kindle-screensaver-converter>original Kindle Screensaver Converter script</a>. The GUI allows users to define target dimensions, resolution, and bit depth while visually interacting with their image collection. A compiled version for Windows is included in the Releases section.
</div>

## Features

- **User-Friendly GUI:** Intuitive interface for managing the screensaver conversion process.
- **Dimension Control:** Set custom target height and width in pixels.
- **Resolution Adjustment:** Define horizontal and vertical resolution (DPI).
- **Bit Depth Configuration:** Customize the bit depth of the output.
- **Smart Cropping:** Automatically detects and retains the most visually prominent area of each image.
- **Grayscale with Contrast Enhancement:** Applies grayscale and enhances contrast for better visual impact.
- **Batch Processing:** Converts multiple images at once.
- **Dark Theme:** Integrated support for a visually appealing dark mode.
- **Output Folder:** Processed images are saved in a `converted_screensavers` folder, which is automatically created in the program's directory if it does not already exist.
- **Executable Compilation:** Includes a `kindle_screensaver.spec` file for compiling the program into an executable.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`
  - Pillow
  - PyQt6
  - pyqtdarktheme
  - numpy

## Installation

### Setting up the Environment

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On **Windows (CMD):**
     ```bash
     venv\Scripts\activate
     ```
   - On **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - On **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the GUI

1. **Prepare Input Images:** Place the images you want to convert in any folder on your system. Alternatively, you can place them in the `PUT YOUR IMAGES HERE` folder if you want the program to load them automatically at startup (the program reads this folder when it starts). 

>If you have a compiled version of the program and want it to load the images automatically at startup, create a folder named `PUT YOUR IMAGES HERE` in the same directory as the program.
2. **Launch the GUI:**
   ```bash
   python kindle-screensaver-converter-gui.py
   ```
3. **Select Input Folder:** Click the `Select Input Folder` button and choose the folder containing your images.
4. **Set Conversion Parameters:** Use the provided fields to define:
   - Target height and width in pixels.
   - Horizontal and vertical DPI.
   - Bit depth.
5. **Start Conversion:** Click `Convert Images` to process your images.
6. **Check Output:** Converted images will be saved in a `converted_screensavers` folder in the program's directory.

### Compiling the Program

The project includes a `kindle_screensaver.spec` file for compiling the program into an executable for your desired operating system using PyInstaller.

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Compile the Program:**
   ```bash
   pyinstaller kindle_screensaver.spec
   ```

3. The compiled executable will be available in the `dist` folder.

### Precompiled Version

A precompiled executable for Windows is available in the Releases section of this repository. Download and run it directly without needing Python or dependencies.

## Example Workflow

1. Place your images in a folder.
2. Run the GUI and select the folder.
3. Define target dimensions, DPI, and bit depth as needed.
4. Start the conversion process.
5. Access the converted images in the `converted_screensavers` folder in the program's directory .

## Troubleshooting

- Ensure that the input folder exists and contains valid image files.
- Verify that Python and the required libraries are installed.
- Check your file permissions for the working directory.
- For compiled versions, ensure compatibility with your operating system.

## Releases

- Precompiled Windows executable available in the Releases section.
- Source code for all platforms is provided.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

