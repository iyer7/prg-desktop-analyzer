# 🔬 Aerosol Jet .prg Analyzer - Desktop Application

**A standalone desktop application (for Windows) to analyze Aerosol Jet Printer (.prg) files, identify mechanical stress points, and calculate the maximum safe printing speed.**

---

## 1. Purpose of This Application

This is a desktop GUI (Graphical User Interface) application created using Python and the PyQt6 framework. It provides a user-friendly interface for analyzing `.prg` files generated for Optomec Aerosol Jet Printers.

Its core goal is to allow users (technicians, researchers) to perform a "digital pre-flight check" on their print designs *before* running them on the actual machine. This helps prevent print failures caused by high-speed movements over sharp corners or non-tangential curves, saving time and materials.

This application runs locally on a Windows computer and does **not** require an internet connection after the initial setup.

---

## 2. Files in this Repository

This GitHub repository contains the source code and configuration needed to build and run the application. The key files are:

* **`app.py`:** The main Python script that defines and runs the Graphical User Interface (GUI) using the PyQt6 library. This creates the window, buttons, text boxes, etc., that the user interacts with.
* **`analyzer_logic.py`:** A separate Python script containing the core "engine" of the application. It handles:
    * Parsing the `.prg` file.
    * Performing all the geometric calculations for stress analysis.
    * Generating the animation frames using Matplotlib.
    * Creating the annotated output file.
    This file is designed to be "headless" (it doesn't contain GUI code itself).
* **`analyzer_config.ini`:** A simple text file used to remember the last G-Factor value entered by the user for convenience. It is automatically created or updated by the application.
* **`README.md`:** This file – providing documentation and instructions.
* **`.gitignore`:** A configuration file for Git (the version control system) specifying which files should *not* be uploaded to this repository (like temporary build files).

**What is NOT included:**
* `build/` folder, `dist/` folder, `PRG_Analyzer.spec` file: These are **temporary files and folders generated** by the `PyInstaller` tool during the process of creating the final `.exe` application (see Section 4). They are not part of the source code and are specific to the machine they were built on, so they are not stored here.

---

## 3. How the Application Works (High-Level Flow)

1.  The user launches the `PRG_Analyzer.exe` application.
2.  The main window appears (created by `app.py`).
3.  The user clicks "Select .prg File" and chooses their file.
4.  The user enters the desired "G-Factor" limit.
5.  The user clicks "Run Analysis".
6.  `app.py` calls functions within `analyzer_logic.py`, passing the filename and G-Factor.
7.  `analyzer_logic.py` performs the parsing, calculations, and animation generation.
8.  `analyzer_logic.py` returns the results (report text, path to annotated file, animation object) back to `app.py`.
9.  `app.py` displays the report in the text box.
10. `app.py` triggers Matplotlib to display the animation in a pop-up window.
11. `app.py` shows a success message indicating where the `_annotated.prg` file was saved.

---

## 4. How to Build the Standalone Windows Application (`.exe`)

This repository contains the *source code*. To create the easy-to-use `.exe` file that can be run on any Windows PC without installing Python, you need to use a tool called `PyInstaller`. This needs to be done **once** on a Windows computer that has internet access.

**Follow these steps exactly on your Windows PC:**

### A. Prerequisites (One-Time Setup)

1.  **Install Python:**
    * Go to [python.org](https://www.python.org/) and download the latest **Python 3** installer for Windows.
    * Run the installer.
    * **CRITICAL:** On the first screen of the installer, check the box at the bottom that says **"Add Python to PATH"**. 
    * Click "Install Now" and complete the installation.
2.  **Install Git:**
    * Go to [git-scm.com/download/win](https://git-scm.com/download/win) and download the Git installer for Windows.
    * Run the installer, accepting the default options is usually fine. Git is needed to download the code from GitHub.
3.  **Open Command Prompt:**
    * Click the Windows Start Menu.
    * Type `cmd` and press Enter. A black command prompt window will open.

### B. Download the Application Code

1.  **Choose a Location:** Decide where you want to put the project code (e.g., your Desktop).
2.  **Navigate in Command Prompt:** Use the `cd` command to move into that location. For example, to go to your Desktop:
    ```cmd
    cd Desktop
    ```
3.  **Clone the Repository:** Copy the code from GitHub using this command (replace `<Your_GitHub_Username>` with your actual username):
    ```cmd
    git clone [https://github.com/](https://github.com/)<Your_GitHub_Username>/prg-desktop-analyzer.git
    ```
    This will create a new folder named `prg-desktop-analyzer` containing all the code files.
4.  **Enter the Project Folder:**
    ```cmd
    cd prg-desktop-analyzer
    ```

### C. Install Required Python Libraries

1.  **Upgrade Pip (Recommended):**
    ```cmd
    python -m pip install --upgrade pip
    ```
2.  **Install Libraries:** Install all the Python packages needed by the application:
    ```cmd
    pip install PyQt6 numpy matplotlib pyinstaller
    ```
    Wait for all installations to complete.

### D. Build the `.exe` Application

1.  **Run PyInstaller:** Execute the following command in the Command Prompt (make sure you are still inside the `prg-desktop-analyzer` folder):
    ```cmd
    pyinstaller --windowed --name="PRG_Analyzer" app.py
    ```
    * `--windowed`: Prevents a black console window from showing up behind the app.
    * `--name="PRG_Analyzer"`: Sets the name of the final executable.
    You will see a lot of text scrolling as PyInstaller analyzes the code and bundles everything. This might take a minute or two.

### E. Locate and Run the Application

1.  **Find the App:** Once PyInstaller finishes, look inside your `prg-desktop-analyzer` folder. You will find a new folder named `dist`. Open it.
2.  **Inside `dist`:** You will see **another folder** named `PRG_Analyzer`. **This folder IS your application.**
3.  **Run:** Open the `PRG_Analyzer` folder. Double-click the file named **`PRG_Analyzer.exe`**.
    
4.  The application GUI should launch!

### F. Sharing the Application (Important!)

* The `PRG_Analyzer.exe` file **needs all the other files and folders** inside that `dist\PRG_Analyzer` directory to work correctly.
* To share the application with someone else (or move it to another PC like the cleanroom computer):
    1.  Go to the `dist` folder.
    2.  Right-click on the **`PRG_Analyzer` folder**.
    3.  Select **"Send to > Compressed (zipped) folder"**.
    4.  Share the resulting **`PRG_Analyzer.zip`** file.
    5.  The recipient just needs to unzip the file and double-click the `.exe` inside. **No Python installation is needed on their end.**

---

## 5. How to Use the Built Application

1.  Double-click `PRG_Analyzer.exe`.
2.  Click "Select .prg File" and choose the file to analyze.
3.  Enter the desired "G-Factor" (e.g., 0.5).
4.  Click "Run Analysis".
5.  View the report in the text area.
6.  Watch the animation in the pop-up window (close it when done).
7.  Find the `_annotated.prg` file saved in the same directory as the original `.prg` file.

---

## 6. Author

* **[Suraj Ramesh Iyer]** - *Initial Work & Development* - [https://github.com/iyer7]
