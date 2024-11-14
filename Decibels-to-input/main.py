import sounddevice as sd
import numpy as np
import pyautogui
import cv2
import threading

# Parameters
duration = 120  # seconds
sampling_rate = 44100  # Hz
block_duration = 0.05  # Block size in seconds (smaller block size for lower latency)
db_threshold_write = 20  # Threshold to trigger pyautogui

# Global variable to store the current decibel value
current_decibels = 0.0

def rms_value(audio_data):
    return np.sqrt(np.mean(audio_data**2))

def calculate_decibels(audio_data, reference=1.0):
    rms = rms_value(audio_data)
    if rms > 0:
        db = 20 * np.log10(rms / reference)
    else:
        db = -np.inf
    return db

def audio_callback(indata, frames, time, status):
    global current_decibels
    if status:
        print(status)
    audio_data = indata[:, 0]
    decibels = calculate_decibels(audio_data, reference=0.01)
    if decibels > -np.inf:
        current_decibels = decibels
        print(f"Decibels: {decibels:.2f} dB")
        if decibels > db_threshold_write:
            print("Condition met, pressing leftclick")
            pyautogui.click(button='left')
            print("pressed leftclick")
        else:
            print("Condition not met")

#display the decibel level on the screen
def display_decibels():
    global current_decibels
    cv2.namedWindow("Decibel Display", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Decibel Display", 300, 100)
    while True:
        img = np.zeros((100, 300, 3), np.uint8)
        text = f"Decibels: {current_decibels:.2f} dB"
        cv2.putText(img, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Decibel Display", img)
        if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cv2.destroyAllWindows()

#choose the microphone
def choose_microphone():
    devices = sd.query_devices()
    input_devices = [device for device in devices if device['max_input_channels'] > 0]
    print("Available input devices:")
    for i, device in enumerate(input_devices):
        print(f"{i}: {device['name']}")
    device_index = int(input("Please choose the device index: "))
    return input_devices[device_index]['name']

# Get the chosen microphone
device_name = choose_microphone()
device_index = sd.query_devices().index(next(device for device in sd.query_devices() if device['name'] == device_name))

if device_index is None:
    print(f"Device '{device_name}' not found.")
else:
    print(f"Using device index: {device_index} for '{device_name}'")

    # Start a thread for the decibel display
    display_thread = threading.Thread(target=display_decibels)
    display_thread.daemon = True
    display_thread.start()

    # Start the audio stream with lower latency settings
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sampling_rate, blocksize=int(sampling_rate * block_duration), device=device_index, latency='low'):
        print(f"Recording from '{device_name}' for {duration} seconds...")
        sd.sleep(duration * 1000)
