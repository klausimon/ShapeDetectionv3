import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import threading
from shapetracker import ShapeTracker


class VideoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Tracking GUI")  # Window title
        self.setup_ui()  # Initialize UI

        self.video_path = ""  # Path to video file
        self.is_playing = False  # Playback state
        self.tracker = ShapeTracker()  # Create shape tracker

    def setup_ui(self):
        self.root.geometry("800x600")  # Initial window size
        self.root.minsize(640, 480)  # Minimum window size

        # Control panel
        control_frame = tk.Frame(self.root)  # Container for buttons
        control_frame.pack(pady=10)

        self.open_btn = tk.Button(control_frame, text="Open Video", command=self.open_video, width=15)
        self.open_btn.pack(side=tk.LEFT, padx=5)  #open button

        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_video, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)  #stop button

        # Video display
        self.video_canvas = tk.Canvas(self.root, bg='black')  # Canvas for video
        self.video_canvas.pack(fill=tk.BOTH, expand=True)  # Fill window

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])  # File dialog
        if self.video_path:
            self.start_video()  # Start playback

    def start_video(self):
        self.cap = cv2.VideoCapture(self.video_path)  # Open video file
        if not self.cap.isOpened():
            return

        self.is_playing = True
        self.open_btn.config(state=tk.DISABLED)  # Disable open button
        self.stop_btn.config(state=tk.NORMAL)  # Enable stop button

        # Start video thread
        self.thread = threading.Thread(target=self.process_video, daemon=True)
        self.thread.start()  # Start processing thread

    def stop_video(self):
        self.is_playing = False  # Stop playback
        self.open_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if hasattr(self, 'cap'):
            self.cap.release()  # Release video capture

    def process_video(self):
        while self.is_playing and self.cap.isOpened():
            ret, frame = self.cap.read()  # Read frame
            if not ret:
                break

            # Processing
            detected_shapes = self.tracker.detect_shapes(frame)  # Detect shapes
            self.tracker.update_tracking(detected_shapes)  # Update trackers
            self.tracker.draw_results(frame)  # Draw results

            # Update display
            self.update_gui(frame)  # Show processed frame

            cv2.waitKey(25)  # Control playback speed

        self.stop_video()

    def update_gui(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert colorspace
        img = Image.fromarray(frame)  # Convert to PIL format
        img.thumbnail((self.video_canvas.winfo_width(), self.video_canvas.winfo_height()))  # Resize

        imgtk = ImageTk.PhotoImage(image=img)  # Convert to Tkinter format
        self.video_canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)  # Display image
        self.video_canvas.image = imgtk  # Keep reference

    def on_closing(self):
        self.stop_video()
        self.root.destroy()  # Close application