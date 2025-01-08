from moviepy.editor import *
import warnings
import os

# Configuration variables
video_path = "sample.mkv"  # Path to your video file
output_audio_path = "extracted_audio.mp3"  # Path to save the extracted audio
start_time = 1190  # Start time in seconds
end_time = 1207  # End time in seconds

def extract_audio(video_path, output_audio_path, start_time, end_time):
    """
    Extracts audio from a video file between specified timestamps.

    :param video_path: Path to the video file.
    :param output_audio_path: Path where the extracted audio will be saved.
    :param start_time: Start timestamp in seconds (e.g., 10 for 10 seconds).
    :param end_time: End timestamp in seconds (e.g., 20 for 20 seconds).
    """
    if not os.path.exists(video_path):
        print(f"Error: The video file {video_path} does not exist.")
        return

    video = None
    try:
        # Suppress warnings about unsupported streams
        warnings.filterwarnings("ignore", category=UserWarning, module="moviepy")

        # Load the video file
        video = VideoFileClip(video_path)

        # Extract the audio
        audio = video.audio

        # Trim the audio between start_time and end_time
        audio = audio.subclip(start_time, end_time)

        # Write the audio to a file
        audio.write_audiofile(output_audio_path)

        print(f"Audio extracted successfully to {output_audio_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the video file to release resources if it was successfully created
        if video:
            video.close()

# Example usage
if __name__ == "__main__":
    extract_audio(video_path, output_audio_path, start_time, end_time)
