import os, time, customtkinter as ct, subprocess
from tkinter import filedialog, StringVar

# UI settings
ct.set_default_color_theme("green")
ct.set_appearance_mode("System")

# Initialize root window
root = ct.CTk()
root.geometry("685x400")
root.title("Skeet GUI Autoloader - 2.0")
root.resizable(False, False)

if not os.path.isfile("config.txt"):  # Check if config file exists
    with open("config.txt", "w") as f: # Create the config file if it doesn't exist
        f.write("")

# Function to change appearance mode
def change_appearance_mode_event(new_appearance_mode: str):
    ct.set_appearance_mode(new_appearance_mode)

def toggle_password_visibility():
    if show_password_var.get() == "yes":
        password_entry.configure(show="")  # show characters
    else:
        password_entry.configure(show="*")  # hide characters

# Function to save the config
def save_config():
    username = username_entry.get() # Get the username
    password = password_entry.get() # Get the password
    insecure = insecure_checkbox.get() # Get the insecure checkbox value
    autoinject = inject_checkbox.get()  # Get the autoinject checkbox value
    file_location = file_location_var.get()  # Get the selected file location
    launch_options = launch_options_entry.get()  # Get the launch options
    with open("config.txt", "w") as f:
        f.write(f"{username}:{password}:{insecure}:{autoinject}\n")  # Save the first line with the username:password:insecure
        f.write(f"{file_location}\n")  # Save the loader path on the second line
        f.write(f"{launch_options}")  # Save the launch options on the third line

# Function to browse and select a file
def browse_file():
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        folder_path = os.path.dirname(file_path)  # Get the directory of the selected file
        file_location_var.set(folder_path)  # Update the StringVar with the selected folder location

# Function to inject skeet
def inject_skeet():
    
    loader_path = file_location_var.get()
    autoinject = inject_checkbox.get()  # Assign the autoinject checkbox value to a variable

    # Execute the .exe in that path with "--load=1" parameter
    for file in os.listdir(loader_path):
        if file.endswith(".exe"):
            exe_path = os.path.join(loader_path, file)
            os.system(f'start "" "{exe_path}" --load=1')
            break

# Function to inject and load csgo
def load_csgo():
    login_username = username_entry.get()
    login_password = password_entry.get()
    launch_options = launch_options_entry.get()
    insecure = insecure_checkbox.get()  # Assign the insecure checkbox value to a variable
    autoinject = inject_checkbox.get()  # Assign the autoinject checkbox value to a variable

    if autoinject == "yes":  # Use the newly assigned variable
        inject_skeet()
    
    # Get the Steam installation path from the registry
    steam_path = ''
    try:
        output = subprocess.check_output('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v "InstallPath"', shell=True)
        output_str = output.decode().strip()
        steam_path = output_str.split('   ')[3].strip()
    except Exception as e:
        print(f'Error retrieving Steam installation path: {e}')
    
    if insecure == "yes":  # Use the newly assigned variable
        launch_options += " -insecure"
    
    if steam_path:
        # Start Steam with login credentials and launch options
        steam_exe_path = os.path.join(steam_path, 'Steam.exe')
        launch_command = f'"{steam_exe_path}" -login {login_username} {login_password} -applaunch 730 {launch_options}'
        os.system(f'start "CSGO" {launch_command}')
    else:
        print('Steam installation path not found')

# Initialize Tabs for UI
tabsFrame = ct.CTkTabview(master=root)
tabsFrame.grid(row=0, column=0, pady=10, padx=30, sticky="nsew")

# Initialize Main Tab
mainTabLabel = tabsFrame.add("Loader")
loaderTab = ct.CTkFrame(master=mainTabLabel)
loaderTab.grid(row=0, column=0, pady=6, padx=5)

# User Credentials under Main Tab
username_label = ct.CTkLabel(master=loaderTab, text="Username")
username_entry = ct.CTkEntry(master=loaderTab)
password_label = ct.CTkLabel(master=loaderTab, text="Password")
password_entry = ct.CTkEntry(master=loaderTab, show="*")
show_password_var = StringVar()
show_password_check = ct.CTkCheckBox(master=loaderTab, text="Show Password", variable=show_password_var, onvalue="yes", offvalue="no", command=toggle_password_visibility)

# Positioning of User Credentials under Main Tab
username_label.grid(row=0, column=0, pady=2, padx=5, sticky="w")
username_entry.grid(row=0, column=1, pady=2, padx=5, sticky="ew")
password_label.grid(row=1, column=0, pady=2, padx=5, sticky="w")
password_entry.grid(row=1, column=1, pady=2, padx=5, sticky="ew")
show_password_check.grid(row=1, column=2, pady=2, padx=5, sticky="w")

# Launch Options under Main Tab
launch_options_label = ct.CTkLabel(master=loaderTab, text="Launch Options")
launch_options_label.grid(row=4, column=0, pady=2, padx=5, sticky="w")
launch_options_entry = ct.CTkEntry(master=loaderTab)
launch_options_entry.grid(row=4, column=1, pady=2, padx=5, sticky="ew")

# Insecure CheckBox under Main Tab
insecure_checkbox = ct.CTkCheckBox(master=loaderTab, text="Insecure")
insecure_checkbox.grid(row=4, column=2, pady=2, padx=5, sticky="w")

# File Location Label under Main Tab
file_location_label = ct.CTkLabel(master=loaderTab, text="Loader Path:")
file_location_label.grid(row=5, column=0, pady=2, padx=5, sticky="w")

# File Location Label under Main Tab
file_location_var = StringVar()
file_location_var.set("Loader path not selected")
file_location_label = ct.CTkLabel(master=loaderTab, textvariable=file_location_var)
file_location_label.grid(row=5, column=1, pady=2, padx=5, sticky="ew")

# Inject CheckBox under Main Tab
inject_checkbox = ct.CTkCheckBox(master=loaderTab, text="Inject")
inject_checkbox.grid(row=4, column=3, pady=2, padx=5, sticky="w")

# Browse, Save, and Load Buttons under Main Tab
browseButton = ct.CTkButton(master=loaderTab, text="Select loader path", command=browse_file)
browseButton.grid(row=6, column=0, pady=2, padx=5)
saveButton = ct.CTkButton(master=loaderTab, text="Save Config", command=save_config)
saveButton.grid(row=6, column=1, pady=2, padx=5)
injectButton = ct.CTkButton(master=loaderTab, text="Inject Skeet", command=inject_skeet)
injectButton.grid(row=6, column=2, pady=2, padx=5)
loadButton = ct.CTkButton(master=loaderTab, text="Load CS:GO", command=load_csgo)
loadButton.grid(row=6, column=3, pady=2, padx=5)

# Container for progress bar and appearance mode selector
container = ct.CTkFrame(master=root)
container.grid(row=1, column=0, pady=10, padx=30, sticky="nsew")

# Initialize Progress Bar
progressbar_1 = ct.CTkProgressBar(master=container)
progressbar_1.grid(row=0, column=0, pady=2, padx=5, sticky="w")
progressbar_1.configure(mode="indeterminate")
progressbar_1.start()

# Initialize Appearance Mode Option
appearance_mode_label = ct.CTkLabel(master=container, text="Appearance Mode")
appearance_mode_label.grid(row=0, column=1, pady=6, padx=5, sticky="w")
appearance_mode_optionmenu = ct.CTkOptionMenu(master=container, values=["System", "Dark", "Light"], command=change_appearance_mode_event)
appearance_mode_optionmenu.grid(row=0, column=2, pady=6, padx=5, sticky="w")

# Initialize Exit Button
exit_button = ct.CTkButton(master=container, text="Exit", command=root.destroy)
exit_button.grid(row=0, column=3, pady=6, padx=5, sticky="e")

# Autologin if config.txt exists
with open("config.txt", "r") as f:
    data = f.read().splitlines()
    fill_data = data[0].split(":")  # Split the first line by colon
    username_entry.insert(0, fill_data[0])  # Insert username
    password_entry.insert(0, fill_data[1])  # Insert password
    if fill_data[2]: # Check if insecure is True
        insecure_checkbox.select()  # Select insecure checkbox
    if fill_data[3]: # Check if inject is True
        inject_checkbox.select()  # Select inject checkbox
    if len(data) >= 2:
        loader_data = data[1]  # Get the second line
        file_location_var.set(loader_data)  # Set the file location
    if len(data) >= 3:
        launch_options_data = data[2]  # Get the third line
        launch_options_entry.insert(0, launch_options_data)  # Insert launch options

# Run the tool & Handle KeyboardInterrupt to exit gracefully
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Detected CTRL+C, exiting...")
    time.sleep(0.5)
    exit()
