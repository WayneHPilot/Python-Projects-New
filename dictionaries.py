import pickle

# Playlist dictionary
playlist ={}

# Function to save playlist to a file
def save_playlist():
    with open("playlist.pkl", "wb") as file:
        pickle.dump(playlist, file)
    print("✅ Playlist has been saved.\n")

# Function to load playlist from a file
def load_playlist():
    try:
        with open("playlist.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}  # Return an empty playlist if the file doesn't exist

# Load playlist when starting the program
playlist = load_playlist()

# Function to add a song to the playlist
def add_song():
    title = input("Enter the song title: ").strip()
    artist = input("Enter the artist name: ").strip()
    genre = input("Enter the genre: ").strip()

    if title in playlist:
        print(f"⚠️ The song '{title}' already exists in the playlist.\n")
        return

    if not title or not artist or not genre:
        print("⚠️ Title, artist, and genre cannot be empty.\n")
        return

    playlist[title] = {"artist": artist, "genre": genre}
    print(f"✅ '{title}' by {artist} added to the playlist.\n")


# Function to view the playlist
def view_playlist():
    try:
        if not playlist:
            raise ValueError
        
        print("\n🎵--- Your Playlist ---")
        for title, info in playlist.items():
            print(f"🎶 Title: {title}, Artist: {info['artist']}, Genre: {info['genre']}")
        print("---------------------\n")
    except ValueError:
        print("⚠️ Your playlist is currently empty. Add some songs!\n")


# Function to update song information
def update_song():
    try:
        title = input("Enter the song title to update: ").strip()
        song = playlist[title]

        artist = input("Enter the new artist (press Enter to skip): ").strip()
        genre = input("Enter the new genre (press Enter to skip): ").strip()

        if artist:
            song["artist"] = artist
        if genre:
            song["genre"] = genre
        
        if not artist and not genre:
            print("⚠️ No updates provided.\n")
            return
        
        print(f"✅ '{title}' has been successfully updated.\n")

    except KeyError:
        print(f"⚠️ The song '{title}' was not found in the playlist.\n")


# Function to delete a song from the playlist
def delete_song():
    try:
        title = input("Enter the song title to delete: ").strip()
        del playlist[title] 
        print(f"✅ '{title}' has been removed from the playlist.\n")

    except KeyError: 
        print(f"⚠️ The song '{title}' was not found in the playlist.\n")

# Menu
def main():
    while True:
        print("📋 Menu:")
        print("1. Add Song")
        print("2. View Playlist")
        print("3. Update Song")
        print("4. Delete Song")
        print("5. Exit")

        try:
            choice = input("Choose an option (1-5): ").strip()
            if choice not in ["1", "2", "3", "4", "5"]:
                raise ValueError  

            if choice == "1":
                add_song()
            elif choice == "2":
                view_playlist()
            elif choice == "3":
                update_song()
            elif choice == "4":
                delete_song()
            elif choice == "5":
                save_playlist()
                print("👋 Exiting the playlist manager. Goodbye!")
                break

        except ValueError:  
            print("⚠️ Invalid choice. Please select a number between 1 and 5.\n")


if __name__ == "__main__":
    main()