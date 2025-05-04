import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os

model = whisper.load_model("large")

def transcribe(file_path):
    result = model.transcribe(
            file_path,
            verbose=True,
            task='transcribe',  # Use 'transcribe' instead of 'translate' if you want output in the original language
            language=None,      # Set to None to enable language detectiono prevent automatic translation
        )

    print(f"Result: {result}")

    srt_path = os.path.splitext(file_path)[0] + ".srt"
    with open(srt_path, "w") as f:
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment['text'].strip()
            lang = segment.get('language')
            f.write(f"{i+1}\n{start} --> {end}\n[{lang}] {text}\n\n")
    messagebox.showinfo("Done", f"Saved: {srt_path}")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".replace('.', ',')

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg")]
    )
    if file_path:
        transcribe(file_path)

root = tk.Tk()
root.title("Convert Audio to SRT")
root.geometry("300x200")

label = tk.Label(root, text="Select an audio file to convert to SRT", wraplength=250)
label.pack(pady=40)

btn = tk.Button(root, text="Select File", command=select_file)
btn.pack(pady=10)

root.mainloop()
