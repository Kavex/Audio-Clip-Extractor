import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os
import warnings
import threading
from datetime import datetime


class AudioExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Clip Extractor by Kavex")

        # Set up configuration variables
        self.video_path = ""
        self.output_folder = ""
        self.start_time = 0
        self.end_time = 0
        self.output_format = "WAV"  # Default output format is WAV
        self.sample_rate = 22050  # Default sample rate is 22050 Hz

        # Video file selection
        self.video_label = tk.Label(root, text="Select Video File:")
        self.video_label.grid(row=0, column=0, padx=10, pady=5)

        self.video_button = tk.Button(root, text="Browse", command=self.browse_video)
        self.video_button.grid(row=0, column=1, padx=10, pady=5)

        # Start and End times input
        self.start_label = tk.Label(root, text="Enter start time (in seconds):")
        self.start_label.grid(row=1, column=0, padx=10, pady=5)

        self.start_entry = tk.Entry(root, width=20)
        self.start_entry.grid(row=1, column=1, padx=10, pady=5)

        self.end_label = tk.Label(root, text="Enter end time (in seconds):")
        self.end_label.grid(row=2, column=0, padx=10, pady=5)

        self.end_entry = tk.Entry(root, width=20)
        self.end_entry.grid(row=2, column=1, padx=10, pady=5)

        # Output folder selection
        self.output_label = tk.Label(root, text="Select Output Folder:")
        self.output_label.grid(row=3, column=0, padx=10, pady=5)

        self.output_button = tk.Button(root, text="Browse", command=self.browse_output_folder)
        self.output_button.grid(row=3, column=1, padx=10, pady=5)

        # Output format selection
        self.format_label = tk.Label(root, text="Select Output Format:")
        self.format_label.grid(row=4, column=0, padx=10, pady=5)

        self.format_options = ["MP3", "WAV"]
        self.format_dropdown = tk.OptionMenu(root, tk.StringVar(value=self.output_format), *self.format_options, command=self.update_output_format)
        self.format_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Sample rate selection
        self.sample_rate_label = tk.Label(root, text="Select Sample Rate (Hz):")
        self.sample_rate_label.grid(row=5, column=0, padx=10, pady=5)

        self.sample_rate_options = [8000, 11025, 16000, 22050, 44100, 48000]
        self.sample_rate_dropdown = tk.OptionMenu(root, tk.IntVar(value=self.sample_rate), *self.sample_rate_options, command=self.update_sample_rate)
        self.sample_rate_dropdown.grid(row=5, column=1, padx=10, pady=5)

        # Progress console
        self.console = tk.Text(root, height=10, width=60, state=tk.DISABLED)
        self.console.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Extract Button
        self.extract_button = tk.Button(root, text="Extract Audio", command=self.extract_audio_thread)
        self.extract_button.grid(row=7, column=0, columnspan=2, pady=20)

    def browse_video(self):
        """Browse for video file."""
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
        if self.video_path:
            self.log(f"Selected video file: {os.path.basename(self.video_path)}")

    def browse_output_folder(self):
        """Browse for output folder."""
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.log(f"Audio files will be saved to: {self.output_folder}")

    def update_output_format(self, choice):
        """Update output format."""
        self.output_format = choice

    def update_sample_rate(self, rate):
        """Update sample rate."""
        self.sample_rate = int(rate)

    def log(self, message):
        """Log messages to the console."""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def extract_audio(self):
        """Extract audio from the video."""
        try:
            self.start_time = float(self.start_entry.get())
            self.end_time = float(self.end_entry.get())

            if self.start_time < 0 or self.end_time < 0:
                raise ValueError("Times must be non-negative.")

            if self.start_time >= self.end_time:
                messagebox.showerror("Invalid Times", "End time must be after start time.")
                return

            # Check if the duration is longer than 20 seconds
            if (self.end_time - self.start_time) > 20:
                self.log("Error: The selected clip duration exceeds 20 seconds.")
                messagebox.showerror("Duration Error", "You can't extract audio longer than 20 seconds.")
                return

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for start and end times.")
            return

        if not self.video_path or not self.output_folder:
            messagebox.showerror("Missing Information", "Please select both a video file and an output folder.")
            return

        try:
            # Suppress warnings about unsupported streams
            warnings.filterwarnings("ignore", category=UserWarning, module="moviepy")

            video = VideoFileClip(self.video_path)
            audio = video.audio

            video_duration = video.duration  # Duration of the video
            self.log(f"Video duration: {video_duration} seconds.")

            # Ensure times are within bounds
            if self.start_time >= video_duration or self.end_time > video_duration:
                messagebox.showerror("Invalid Time Range", "The start or end time is out of the video's duration.")
                return

            self.log(f"Extracting audio from {self.start_time}s to {self.end_time}s...")

            # Extract the audio clip in a separate thread
            self.extract_clip_audio(audio)

            video.close()
            self.log("Audio extraction completed.")
            messagebox.showinfo("Success", "Audio extraction completed.")

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def extract_audio_thread(self):
        """Run audio extraction in a separate thread to prevent freezing."""
        extract_thread = threading.Thread(target=self.extract_audio)
        extract_thread.start()

        # Show progress updates
        self.root.after(100, self.check_thread, extract_thread)

    def check_thread(self, thread):
        """Check if the thread is still running and handle any errors."""
        if thread.is_alive():
            self.root.after(100, self.check_thread, thread)

    def extract_clip_audio(self, audio):
        """Extract the audio clip from the video."""
        try:
            # Extract the audio for the given time range
            audio_clip = audio.subclip(self.start_time, self.end_time)

            if audio_clip is None:
                raise Exception("Audio clip extraction failed.")

            # Get the current date and time for the filename
            current_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

            # Create output filename
            output_file = os.path.join(self.output_folder, f"extracted_audio_{self.start_time}_{self.end_time}_{current_time}.{self.output_format.lower()}")

            if self.output_format == "MP3":
                # For MP3, we use the codec parameter
                audio_clip.write_audiofile(output_file, codec="mp3", ffmpeg_params=["-ar", str(self.sample_rate)])
            else:
                # For WAV, we do not specify codec, as it's not necessary
                audio_clip.write_audiofile(output_file, ffmpeg_params=["-ar", str(self.sample_rate)])

            # Log the result
            self.log(f"Extracted audio from {self.start_time}s to {self.end_time}s -> {output_file}")
        except Exception as e:
            self.log(f"Error extracting audio: {e}")
            messagebox.showerror("Error", f"An error occurred while extracting the audio: {e}")


if __name__ == "__main__":
    # Initialize the tkinter window
    root = tk.Tk()
    app = AudioExtractorApp(root)
    root.mainloop()
