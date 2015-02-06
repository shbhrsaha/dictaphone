# dictaphone
Stop-go recording of audio in terminal

Tape Recorder lets you record audio by pressing <Enter> to start/stop recording as many times as you like. At the end of each session, Tape Recorder saves your audio to a WAV file.

PortAudio and PyAudio are required.

Usage:

    python dictaphone.py [output WAV file]

Press <Enter> to start and stop recording. Press CTRL+C to end the session. Intermediary WAV files are saved in the `scratch` folder.
