# ARK: Survival Ascended Game.ini Generator GUI

Welcome to the ARK: Survival Ascended Game.ini Generator! This simple tool helps you create and customize your `Game.ini` configuration file for ARK: Survival Ascended servers, without manually searching and editing each option in a text file.

## What is this tool?

This program is a graphical user interface (GUI) that allows you to:
* Browse a list of important ARK server options.
* See a description of each option and its impact on gameplay.
* Easily set values for these options using input fields or checkboxes.
* Generate a complete `Game.ini` file that you can directly use on your server.

## Features

* **Clear List:** All important configuration options at a glance.
* **Detailed Explanations:** For each option, it explains what it does and how its values affect the game (e.g., "Higher value = faster").
* **Easy Input:** Conveniently adjust values via the GUI.
* **Automatic .ini Generation:** Creates a correctly formatted `Game.ini` file for saving.

## How to Use the Script (for Non-Developers)

There are two main ways to use this script:

### Method 1: Run the Python Script Directly (Recommended for those with Python installed)

This is the easiest way if you already have Python on your computer.

1.  **Download the script:**
    * Go to this GitHub repository.
    * Click on the green **"<> Code"** button in the upper right and select **"Download ZIP"**.
    * Unzip the downloaded ZIP file into a folder of your choice (e.g., `C:\ARK_INI_Tool`).

2.  **Open your command line/PowerShell:**
    * Open the Start menu and search for "cmd" (Command Prompt) or "PowerShell". Click on it.

3.  **Navigate to the script folder:**
    * In the black window, type the command `cd` (for "change directory") followed by the path to the folder where you unzipped the script. Press Enter.
        ```bash
        cd C:\ARK_INI_Tool\ARK-GameINI-GUI-main # Adjust the path as needed!
        ```

4.  **Start the program:**
    * Now, type the following command and press Enter:
        ```bash
        python ark_ini_gui.py
        ```
    * The ARK Game.ini Generator GUI window should open.

### Method 2: Use the Program as a Ready-to-Use .exe File (if available)

If the developer has provided a pre-compiled `.exe` file, this is the easiest way as you don't need a Python installation.

1.  **Download the .exe file:**
    * In this GitHub repository, go to the **"Releases"** tab (usually on the right sidebar or in the top navigation bar).
    * Find the latest version (e.g., `v1.0.0`).
    * Download the `.exe` file (e.g., `ark_ini_gui.exe`) under "Assets".
    * Save the `.exe` file to a folder of your choice.

2.  **Start the program:**
    * Simply navigate to the folder where you saved the `.exe` in your file explorer and double-click it.
    * The ARK Game.ini Generator GUI window should open.

## How to Use the GUI

1.  **Select an Option:** On the left side, you'll see a list of all available configuration options. Click on an option you want to customize.
2.  **View Details:** On the right side, details for the selected option will be displayed:
    * **"Option Name"**: The name of the option as it appears in the `Game.ini`.
    * **"Current Value"**: This is where you enter the desired value.
        * For **True/False** options, a checkbox will appear.
        * For numeric values (multipliers, time values), enter the number.
        * For more complex options (like overriding item stacks or engrams), you must enter the **exact syntax** described under "Value Impact". These options often require a line starting and ending with parentheses `(...)`.
    * **"Description"**: An explanation of what this option does in the game.
    * **"Value Impact"**: A brief note on how higher or lower values affect the game (e.g., "Higher value = more resources", "1.0 is normal"). Pay close attention to the explanations here, especially for complex options!
3.  **Adjust Values:** Change the values as desired. Your current value is automatically saved in the background as soon as you leave the field or change the checkbox.
4.  **Generate Game.ini:** Once you've adjusted all desired options, click the **"Generate Game.ini"** button at the bottom.
5.  **Save:** A window will pop up asking you to choose where to save the `Game.ini` file. Select a location and click "Save".

## Where to Place the Generated `Game.ini`?

The generated `Game.ini` file needs to be copied to the correct folder on your ARK: Survival Ascended server. The default path is usually:

`[YOUR_SERVER_INSTALLATION_DIRECTORY]\ShooterGame\Saved\Config\WindowsServer\`

* **Example:** `C:\Steam\steamapps\common\ARK Survival Ascended Dedicated Server\ShooterGame\Saved\Config\WindowsServer\Game.ini`

**Important:**
* Always back up your existing `Game.ini` before overwriting it!
* Your server may need to be restarted for the changes to take effect.

## For Developers and Interested Users (Git Usage)

If you wish to develop the script yourself or get the latest changes from GitHub, use Git.

### Fetching Changes from GitHub (Pull)

When the developer (or you yourself) make updates to the script, you can bring these updates into your local directory:

1.  **Open your terminal** in the folder of your cloned repository (e.g., `C:\Users\YourName\PycharmProjects\Ark Game.ini Generator`).
2.  **Fetch the latest changes:**
    ```bash
    git pull origin main
    ```
    This command downloads the latest changes from the `main` branch of the GitHub repository and merges them with your local code.

### Uploading Your Changes to GitHub (Push)

If you make changes to the code and want to share them on GitHub:

1.  **Save your changes** in the code.
2.  **Add the changed files to the staging area:**
    ```bash
    git add . # Adds all new/modified files not excluded by .gitignore
    ```
3.  **Create a commit:**
    ```bash
    git commit -m "Brief description of your changes"
    ```
    Replace "Brief description of your changes" with a meaningful message.
4.  **Upload your changes to GitHub:**
    ```bash
    git push origin main
    ```
    This sends your local commits to the `main` branch on GitHub.

## How to Create an .exe File Yourself

If you don't want to require a Python installation on other computers, you can create a standalone `.exe` file. For this, you need the `PyInstaller` tool.

1.  **Install PyInstaller:**
    Make sure you have Python installed and PyInstaller installed:
    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to the script folder:**
    Open your terminal and change to the folder where `ark_ini_gui.py` is saved:
    ```bash
    cd /path/to/your/script/folder
    ```

3.  **Create the .exe file:**
    For a single, executable file without a console window, type:
    ```bash
    pyinstaller --onefile --noconsole ark_ini_gui.py
    ```
    After the process is complete, you will find `ark_ini_gui.exe` in the `dist` subfolder of your project folder.

---

Enjoy customizing your ARK: Survival Ascended server!