import os
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

video_path = None
output_dir = None
counter = 0

def process_video():

    global video_path, output_dir, counter

    if not video_path or not output_dir:
        messagebox.showwarning("Input Needed", "Please select a video and output directory.")
        return
    
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while video.isOpened():
        ret, frame = video.read()
        frame_id = video.get(cv2.CAP_PROP_POS_FRAMES)
        if not ret:
            break
        
        if int(frame_id) % (fps * 5) == 0:
            save_path = os.path.join(output_dir, f"{counter}.png")
            cv2.imwrite(save_path, frame)
            counter += 1

        progress = (frame_id / total_frames) * 100
        progress_var.set(progress)
        progress_bar.update()

    video.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Completed", "Video processing completed!")

def select_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        video_label.config(text=f"Selected Video: {os.path.basename(video_path)}")

def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_label.config(text=f"Output Directory: {output_dir}")

root = tk.Tk()
root.iconbitmap('./framify.ico')
root.title("Framify - Video Frames Extractor")

root.geometry("400x350")

video_label = tk.Label(root, text="Select a video file to process", font=("Helvetica", 12))
video_label.pack(pady=10)

select_video_btn = tk.Button(root, text="Select Video", command=select_video, font=("Helvetica", 12), width=20)
select_video_btn.pack(pady=10)

output_label = tk.Label(root, text="Select the directory to save images", font=("Helvetica", 12))
output_label.pack(pady=10)

select_output_btn = tk.Button(root, text="Select Output Directory", command=select_output_dir, font=("Helvetica", 12), width=20)
select_output_btn.pack(pady=10)

process_btn = tk.Button(root, text="Start Processing", command=process_video, font=("Helvetica", 12), width=20)
process_btn.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=20, fill='x')


root.mainloop()
