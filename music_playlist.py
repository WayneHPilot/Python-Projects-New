import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle

# Load playlist from file
def load_playlist():
    try:
        with open("playlist.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

# Save playlist to file
def save_playlist():
    with open("playlist.pkl", "wb") as file:
        pickle.dump(playlist, file)

# Add a new song
def add_song():
    title = simpledialog.askstring("Add Song", "Enter song title:").strip()
    artist = simpledialog.askstring("Add Song", "Enter artist name:").strip()
    genre = simpledialog.askstring("Add Song", "Enter genre:").strip()

    if not title or not artist or not genre:
        messagebox.showwarning("Warning", "Title, artist, and genre cannot be empty.")
        return

    if title in playlist:
        messagebox.showwarning("Warning", f"'{title}' already exists in the playlist.")
        return

    playlist[title] = {"artist": artist, "genre": genre}
    update_listbox()
    save_playlist()
    messagebox.showinfo("Success", f"'{title}' added to the playlist.")

# Update song details
def update_song():
    selected_song = listbox.get(tk.ACTIVE)
    if not selected_song:
        messagebox.showwarning("Warning", "Please select a song to update.")
        return

    title = selected_song.split(" - ")[0]  # Extract title from listbox
    artist = simpledialog.askstring("Update Song", "Enter new artist (or leave blank):").strip()
    genre = simpledialog.askstring("Update Song", "Enter new genre (or leave blank):").strip()

    if not artist and not genre:
        messagebox.showwarning("Warning", "No updates provided.")
        return

    if artist:
        playlist[title]["artist"] = artist
    if genre:
        playlist[title]["genre"] = genre

    update_listbox()
    save_playlist()
    messagebox.showinfo("Success", f"'{title}' updated successfully.")

# Delete a song
def delete_song():
    selected_song = listbox.get(tk.ACTIVE)
    if not selected_song:
        messagebox.showwarning("Warning", "Please select a song to delete.")
        return

    title = selected_song.split(" - ")[0]  # Extract title from listbox
    del playlist[title]
    
    update_listbox()
    save_playlist()
    messagebox.showinfo("Success", f"'{title}' removed from the playlist.")

# Update the listbox display
def update_listbox():
    listbox.delete(0, tk.END)
    for title, info in playlist.items():
        listbox.insert(tk.END, f"{title} - {info['artist']} ({info['genre']})")

# Exit the program
def exit_program():
    save_playlist()
    root.quit()

# Initialize GUI
root = tk.Tk()
root.title("Playlist Manager")
root.geometry("500x400")

playlist = load_playlist()

# Title Label
tk.Label(root, text="🎵 Playlist Manager", font=("Arial", 14, "bold")).pack(pady=10)

# Listbox to show playlist
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)
update_listbox()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="➕ Add Song", command=add_song, width=15).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="✏️ Update Song", command=update_song, width=15).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="❌ Delete Song", command=delete_song, width=15).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="🚪 Exit", command=exit_program, width=15).grid(row=1, column=1, padx=5, pady=5)

# Run the GUI
root.mainloop()