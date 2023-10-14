import time
import numpy as np
import pyaudiowpatch as pyaudio
import config

IS_STREAMING = False

def list_input_devices():
    p = pyaudio.PyAudio()
    dev_dict = {}
    wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    # list all WASAPI devices
    for i in range(wasapi_info['deviceCount']):
        device = p.get_device_info_by_host_api_device_index(wasapi_info['index'], i)
        if device['maxInputChannels'] > 0:
            dev_dict[device['index']] = device['name']

    return dev_dict

def start_stream(callback, device_index):
    global IS_STREAMING
    p = pyaudio.PyAudio()
    device = p.get_device_info_by_index(device_index)
    frames_per_buffer = int(config.MIC_RATE / config.FPS)
    if device['isLoopbackDevice']:
        stream = p.open(format=pyaudio.paInt16,
                    channels=device['maxInputChannels'],
                    rate=int(device['defaultSampleRate']),
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=device['index'])
    else:
        stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(device['defaultSampleRate']),
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=device['index'])
    overflows = 0
    prev_ovf_time = time.time()
    IS_STREAMING = True
    while IS_STREAMING:
        if device['isLoopbackDevice']:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            y = np.frombuffer(data, dtype=np.int16)[::device['maxInputChannels']].astype(np.float32) 
        else:
            y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)

        callback(y)

    stream.stop_stream()
    stream.close()
    p.terminate()

def stop_stream():
    global IS_STREAMING
    IS_STREAMING = False

if __name__ == '__main__':
    # Start listening to live audio stream
    #start_stream(None)
    list_input_devices()
    start_stream(None, 18)
