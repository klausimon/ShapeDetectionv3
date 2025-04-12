import tkinter as tk
from ui import VideoGUI  # Import GUI class

def main():
    root = tk.Tk()  # Create main window
    app = VideoGUI(root)  # Initialize GUI
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window close
    root.mainloop()  # Start GUI event loop

if __name__ == "__main__":
    main()