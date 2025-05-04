import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os

model = whisper.load_model("large")

def transcribe(file_path):
    top_languages = identify_top_languages(file_path)
    target_directory = os.path.splitext(file_path)[0]

    for i, language in enumerate(top_languages):
        transcribe_one(file_path, language)
    messagebox.showinfo("Transcription Complete", f"Transcription for {', '.join(top_languages)} saved in: {target_directory}")

def transcribe_one(file_path, language):
    result = model.transcribe(
            file_path,
            verbose=True,
            task='transcribe',
            language=language
        )
    build_srt_file(file_path, result, language)

def build_srt_file(file_path, result, language):
    srt_path = get_srt_path(file_path, language)

    with open(srt_path, "w") as f:
        for i, segment in enumerate(result["segments"]):
            f.write(build_srt_file_line(segment, i, language))

def build_srt_file_line(segment, i, language):
    start = format_time(segment["start"])
    end = format_time(segment["end"])
    text = segment['text'].strip()
    lang = segment.get('language', language)
    return f"{i+1}\n{start} --> {end}\n[{lang}] {text}\n\n"

def get_srt_path(file_path, language):
    file_location_name = os.path.splitext(file_path)[0]
    directory_name = file_location_name
    file_name = os.path.basename(file_location_name)

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    srt_path = os.path.join(directory_name, file_name + f".{language}" + ".srt")
    return srt_path

def identify_top_languages(file_path):
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)

    # Get top 3 languages with highest probabilities
    top_3_languages = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_language_codes = [lang for lang, prob in top_3_languages]

    print(f"Top 3 detected languages: {top_3_language_codes}")
    return top_3_language_codes

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

def runInMacOS():
    root = tk.Tk()
    root.title("Convert Audio to SRT")
    root.geometry("300x200")

    label = tk.Label(root, text="Select an audio file to convert to SRT", wraplength=250)
    label.pack(pady=40)

    btn = tk.Button(root, text="Select File", command=select_file)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    runInMacOS()
