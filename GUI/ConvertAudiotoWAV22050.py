import os
import ffmpeg
from tkinter import Tk, filedialog, Button, Label, Checkbutton, IntVar

def select_input_folder():
    folder_selected = filedialog.askdirectory(title="Select Input Folder")
    input_folder_label.config(text=folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory(title="Select Output Folder")
    output_folder_label.config(text=folder_selected)

def convert_files_to_wav():
    input_folder = input_folder_label.cget("text")
    output_folder = output_folder_label.cget("text")
    
    if not input_folder or not output_folder:
        result_label.config(text="Please select both input and output folders.")
        return
    
    # Collect selected formats
    formats_to_convert = []
    if mp3_var.get():
        formats_to_convert.append('.mp3')
    if aac_var.get():
        formats_to_convert.append('.aac')
    if ogg_var.get():
        formats_to_convert.append('.ogg')
    if alac_var.get():
        formats_to_convert.append('.alac')
    if m4a_var.get():
        formats_to_convert.append('.m4a')

    if not formats_to_convert:
        result_label.config(text="Please select at least one format to convert.")
        return

    # Find files to convert
    files_to_convert = []
    for ext in formats_to_convert:
        files_to_convert.extend([f for f in os.listdir(input_folder) if f.lower().endswith(ext)])

    if not files_to_convert:
        result_label.config(text="No files found in the selected formats.")
        return

    # Process the conversion
    for file in files_to_convert:
        file_path = os.path.join(input_folder, file)
        wav_file = file.replace(file.split('.')[-1], 'wav')
        wav_path = os.path.join(output_folder, wav_file)

        try:
            # Use ffmpeg to convert to WAV
            ffmpeg.input(file_path).output(wav_path, ar='22050').run()
        except ffmpeg.Error as e:
            result_label.config(text=f"Error converting {file}: {e}")
            return

    result_label.config(text="Conversion complete!")

# Create the main window
root = Tk()
root.title("Audio File to WAV Converter")

# Set window size (double the default width, with a reasonable height)
root.geometry("400x450")  # 800x400 is wider than the default size (e.g., 400x400)

# Add checkboxes for file formats (above the input button)
mp3_var = IntVar()
aac_var = IntVar()
ogg_var = IntVar()
alac_var = IntVar()
m4a_var = IntVar()

Checkbutton(root, text="MP3", variable=mp3_var).pack()
Checkbutton(root, text="AAC", variable=aac_var).pack()
Checkbutton(root, text="OGG", variable=ogg_var).pack()
Checkbutton(root, text="ALAC", variable=alac_var).pack()
Checkbutton(root, text="M4A", variable=m4a_var).pack()

Label(root, text="Select Input Folder").pack(pady=5)
Button(root, text="Browse Input Folder", command=select_input_folder).pack(pady=5)
input_folder_label = Label(root, text="No folder selected")
input_folder_label.pack(pady=5)

Label(root, text="Select Output Folder").pack(pady=5)
Button(root, text="Browse Output Folder", command=select_output_folder).pack(pady=5)
output_folder_label = Label(root, text="No folder selected")
output_folder_label.pack(pady=5)

Button(root, text="Convert to WAV", command=convert_files_to_wav).pack(pady=20)
result_label = Label(root, text="")
result_label.pack(pady=5)

# Start the GUI loop
root.mainloop()
