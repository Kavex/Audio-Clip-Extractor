
![image](https://github.com/user-attachments/assets/36cba7ef-cc0c-4a94-8d74-7dd05fd5dd43)

# Audio Clip Extractor by Kavex

A simple desktop application built with Tkinter and MoviePy to extract short audio clips from video files. The tool allows users to specify the start and end times (up to 20 seconds) for the extraction, choose between MP3 and WAV output formats, and set the sample rate for the audio.

## Features

- **Graphical User Interface:** Easy-to-use interface built with Tkinter.
- **Flexible Extraction:** Extract audio segments by specifying start and end times in seconds.
- **Output Format Options:** Supports both MP3 and WAV formats.
- **Custom Sample Rates:** Choose from various sample rates (e.g., 8000, 11025, 16000, 22050, 44100, 48000 Hz).
- **Threaded Processing:** Extraction runs in a separate thread to prevent UI freezing.
- **Real-time Logging:** A console within the UI logs the extraction process and any errors.

## Requirements

- **Python 3.x**  
- **Tkinter:** Usually included with Python installations.
- **MoviePy:** For handling video and audio processing.  
- **FFmpeg:** Required by MoviePy for audio extraction. Make sure FFmpeg is installed and added to your system's PATH.
- **Other Standard Libraries:** `os`, `threading`, `datetime`, and `warnings`.


Bonus app: Timestamp tool for lazy calculations 

![image](https://github.com/user-attachments/assets/ddfec903-22d2-425b-9ab5-553bbb60f3e6)
