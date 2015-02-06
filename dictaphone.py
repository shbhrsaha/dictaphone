"""
    Records audio to a WAV file

    Usage:
        python dictaphone.py [output WAV file]
"""

import sys
import os
import time
import thread
import pyaudio
import wave
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
THRESHOLD_MULTIPLIER = 6
THRESHOLD_TIME = 3

audio = pyaudio.PyAudio()
counter = 0

def input_thread(L):
    raw_input()
    L.append(None)

def play(wave_filename):
    """
        Plays a WAV file
    """
    wf = wave.open(wave_filename, 'rb')

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()


def record(output_filename):
    """
        Records audio until key pressed, then saves to file
    """
    global counter

    play("beep_hi.wav")
    print "Recording... Press <Enter> to stop"
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    L = []
    thread.start_new_thread(input_thread, (L,))
    while True:
        if L:
            break
        data = stream.read(CHUNK)
        frames.append(data)

    play("beep_lo.wav")
    print "Stopped recording."

    # save the audio data
    wf = wave.open("scratch/%s.wav" % counter, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    counter += 1

    print "Recording saved."

if __name__ == "__main__":

    if not os.path.exists("scratch"):
        os.makedirs("scratch")

    output_filename = sys.argv[1]

    try:
        while True:
            enter = raw_input("Press <Enter> to start recording \n")
            record(output_filename)
    except KeyboardInterrupt:
        pass

    data= []
    for i in range(counter):
        w = wave.open("scratch/%s.wav" % i, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    output = wave.open(output_filename, 'wb')
    output.setparams(data[0][0])
    for i in range(counter):
        output.writeframes(data[i][1])
    output.close()
