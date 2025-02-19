import tkinter as tk
from tkinter import messagebox, filedialog
import psutil
import os
import shutil
import zipfile
from tkinter import ttk


# Create and return the main window with specified title and dimensions
def create_window():
    window = tk.Tk()
    window.title("Automated File System Cleaner")
    window.geometry("600x500")
    window.config(bg="#f0f0f0")  # Set background color for the window

    # Create a frame to hold the Text widget and the Scrollbar
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Create the Text widget for logs (this is the only one we need)
    global log_text
    log_text = tk.Text(frame, height=8, width=50, wrap=tk.WORD, state=tk.DISABLED, bg="#f9f9f9", fg="black", font=("Arial", 10))
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create the Scrollbar widget and link it to the Text widget
    scrollbar = tk.Scrollbar(frame, command=log_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Text widget to use the Scrollbar
    log_text.config(yscrollcommand=scrollbar.set)

    return window

log_text = None  # Global variable for the log text box
log_window = None # Global variable to track if the log window is open


# Update the log with a new message and scroll to the bottom
def update_log(message):
    log_text.config(state=tk.NORMAL)  # Enable writing to the Text box
    log_text.insert(tk.END, message + "\n")  # Insert the message at the end
    log_text.yview(tk.END)  # Scroll to the bottom
    log_text.config(state=tk.DISABLED)  # Disable editing again


# Clean temporary files from common system directories
def clean_temp_files(window, progress_bar):
    update_log("Starting temporary file cleanup...")
    
    # List of temporary directories to clean
    temp_dirs = [
        os.environ.get('TEMP', '/tmp'),
        os.environ.get('TMP', '/tmp'),
        os.path.expanduser("~/.cache"),
    ]

    total_files = 0  # Count the files to track progress
    files_deleted = 0  # Track the number of files deleted

    # Loop through temp directories and delete files
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for dirpath, _, filenames in os.walk(temp_dir):
                total_files += len(filenames)

    # Start deleting files and updating the progress bar
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for dirpath, _, filenames in os.walk(temp_dir):
                for filename in filenames:
                    try:
                        os.remove(os.path.join(dirpath, filename))
                        files_deleted += 1
                        progress_bar['value'] = (files_deleted / total_files) * 100
                        window.update_idletasks()
                    except Exception as e:
                        update_log(f"Failed to delete {filename}: {e}")

    update_log(f"Cleanup completed. {files_deleted} files deleted.")
    progress_bar['value'] = 100


# Check and display the system's disk space usage
def check_disk_space(window, progress_bar):
    update_log("Checking disk space for all drives...")  # Log the start of the disk space check

    # Get all mounted partitions
    partitions = psutil.disk_partitions()

    # Total number of partitions for progress bar
    total_partitions = len(partitions)
    partitions_checked = 0

    for partition in partitions:
        # Check disk usage for each partition
        disk_usage = psutil.disk_usage(partition.mountpoint)

        # Log the disk space information for each drive
        update_log(f"\nDrive: {partition.device}")
        update_log(f"Total: {disk_usage.total // (1024 ** 3)} GB")
        update_log(f"Used: {disk_usage.used // (1024 ** 3)} GB")
        update_log(f"Free: {disk_usage.free // (1024 ** 3)} GB")
        update_log(f"Percentage used: {disk_usage.percent}%")
        
        # Log a warning if disk usage exceeds 80%
        if disk_usage.percent > 80:
            update_log(f"Warning: Disk usage above 80% for {partition.device}")

        # Update progress bar
        partitions_checked += 1
        progress_bar['value'] = (partitions_checked / total_partitions) * 100
        window.update_idletasks()

    update_log("Disk space check complete.")
    progress_bar['value'] = 100  # Set progress bar to 100% when done


# Backup files from a user-specified directory
def backup_old_files(window, progress_bar):
    update_log("Starting backup of old files...")

    # Ask the user to select a directory to back up
    source_dir = filedialog.askdirectory(title="Select Directory to Backup")
    if not source_dir:
        update_log("No directory selected. Backup aborted.")
        return
    
    # Ask where to save the backup
    backup_dir = filedialog.askdirectory(title="Select Backup Destination")
    if not backup_dir:
        update_log("No backup destination selected. Backup aborted.")
        return

    # Use shutil to copy the directory to a temporary backup location
    temp_backup_dir = os.path.join(backup_dir, "temp_backup")
    
    try:
        shutil.copytree(source_dir, temp_backup_dir)  # Copy the entire directory
        update_log(f"Temporary backup created at {temp_backup_dir}")

        # Now create the zip backup of the copied directory
        backup_file = os.path.join(backup_dir, f"backup_{os.path.basename(source_dir)}.zip")
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_files = sum([len(files) for _, _, files in os.walk(temp_backup_dir)])
            files_backed_up = 0

            for dirpath, _, filenames in os.walk(temp_backup_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    zipf.write(file_path, os.path.relpath(file_path, temp_backup_dir))
                    files_backed_up += 1
                    progress_bar['value'] = (files_backed_up / total_files) * 100
                    window.update_idletasks()

            update_log(f"Backup completed. {files_backed_up} files backed up.")
        
        # Remove the temporary backup folder after zipping
        shutil.rmtree(temp_backup_dir)  # Remove the temporary backup folder
        update_log(f"Temporary backup directory removed: {temp_backup_dir}")
    
    except Exception as e:
        update_log(f"Backup failed: {e}")
    
    progress_bar['value'] = 100


# Create and return a progress bar widget
def create_progress_bar(window):
    progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
    progress_bar.pack(pady=20)
    return progress_bar


# Create a clear log function to clear the window
def clear_log():
    log_text.config(state=tk.NORMAL)  # Allow modification
    log_text.delete("1.0", tk.END)  # Clear all text
    log_text.config(state=tk.DISABLED)  # Set back to read-only


# Create buttons for each action (clean, analyse disk, backup, view log)
def create_buttons(window, progress_bar):
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=10, padx=20, fill=tk.X)

    cleanup_button = tk.Button(button_frame, text="Clean Temporary Files", command=lambda: run_with_progress(window, progress_bar, clean_temp_files), width=30, bg="#4CAF50", fg="white", font=("Arial", 10), relief="flat")
    cleanup_button.grid(row=0, column=0, padx=5, pady=5)

    disk_analysis_button = tk.Button(button_frame, text="Analyse Disk Space", command=lambda: run_with_progress(window, progress_bar, check_disk_space), width=30, bg="#2196F3", fg="white", font=("Arial", 10), relief="flat")
    disk_analysis_button.grid(row=0, column=1, padx=5, pady=5)

    backup_button = tk.Button(button_frame, text="Backup Old Files", command=lambda: run_with_progress(window, progress_bar, backup_old_files), width=30, bg="#FFC107", fg="white", font=("Arial", 10), relief="flat")
    backup_button.grid(row=1, column=0, padx=5, pady=5)

    log_button = tk.Button(button_frame, text="View Log", command=view_log, width=30, bg="#9C27B0", fg="white", font=("Arial", 10), relief="flat")
    log_button.grid(row=1, column=1, padx=5, pady=5)

    clear_log_button = tk.Button(button_frame, text="Clear Log", command=clear_log, width=30, bg="#f44336", fg="white", font=("Arial", 10), relief="flat")
    clear_log_button.grid(row=2, column=0, padx=5, pady=5)


# Display the current log in a pop-up window
def view_log():
    global log_window
    
    # Check if the log window is already open
    if log_window is not None and log_window.winfo_exists():
        # If the log window exists, just bring it to the front
        log_window.lift()
        return

    # Create a new top-level window for the log
    log_window = tk.Toplevel(window)
    log_window.title("View Log")
    log_window.geometry("600x400")
    
    # Set a custom background color and font for the log window for a cleaner look
    log_window.config(bg="#f9f9f9")

    # Create a Text widget with a Scrollbar for displaying the log
    log_textbox = tk.Text(log_window, wrap=tk.WORD, height=15, width=60, state=tk.NORMAL, bg="#f9f9f9", fg="black", font=("Arial", 10))
    log_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add a Scrollbar for the Text widget
    scrollbar = tk.Scrollbar(log_window, command=log_textbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_textbox.config(yscrollcommand=scrollbar.set)

    # Insert the current log content into the Text widget
    log_textbox.insert(tk.END, log_text.get("1.0", tk.END))
    log_textbox.config(state=tk.DISABLED)  # Make the log read-only

    # When the log window is closed, set the global variable to None
    log_window.protocol("WM_DELETE_WINDOW", lambda: close_log_window(log_window))

    # Wait for the user to close the log window
    log_window.mainloop()

def close_log_window(log_window):
    log_window.quit()
    log_window.destroy()
    log_window = None  # Reset the global variable when the window is closed



# Run a task with progress bar updates
def run_with_progress(window, progress_bar, task_func):
    clear_log()  # Clear log before running any task
    progress_bar['value'] = 0  # Reset the progress bar
    progress_bar.start()  # Start the progress bar
    task_func(window, progress_bar)  # Execute the task
    progress_bar.stop()  # Stop the progress bar


# Main function to initialize and start the application
def main():
    global window, progress_bar
    window = create_window()  # This already initializes log_text as a global variable

    # Initialize the progress bar
    progress_bar = create_progress_bar(window)

    # Create buttons for actions
    create_buttons(window, progress_bar)

    window.mainloop()


if __name__ == "__main__":
    main()
