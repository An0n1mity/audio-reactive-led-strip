import time
import numpy as np
import pyaudiowpatch as pyaudio
import config

# constant to define if loopback device is used or microphone
USE_LOOPBACK = False

def start_stream(callback):
    p = pyaudio.PyAudio()
    # Get default WASAPI info
    if USE_LOOPBACK:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        # Get default WASAPI speakers
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
        
        frames_per_buffer = int(config.MIC_RATE / config.FPS)
        stream = p.open(format=pyaudio.paInt16,
                        channels=default_speakers['maxInputChannels'],
                        rate=config.MIC_RATE,
                        input=True,
                        input_device_index=default_speakers['index'],
                        frames_per_buffer=frames_per_buffer
                        )
    else:
        frames_per_buffer = int(config.MIC_RATE / config.FPS)
        stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    overflows = 0
    prev_ovf_time = time.time()

    while True:
        try:
            if USE_LOOPBACK:
                data = stream.read(frames_per_buffer, exception_on_overflow=False)
                y = np.frombuffer(data, dtype=np.int16)[::default_speakers['maxInputChannels']].astype(np.float32) 
            else:
                y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
                y = y.astype(np.float32)
            callback(y)
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    # Start listening to live audio stream
    start_stream(None)
