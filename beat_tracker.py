#
# Track the tempo of music through the microphone.
#
# https://librosa.github.io/librosa/generated/librosa.beat.beat_track.html
# https://librosa.github.io/librosa/generated/librosa.feature.rmse.html
#
import threading
import math
import numpy
import pyaudio
import librosa


def roundup(x, interval):
    rem = x % interval
    if rem < (interval / 2):
        return int(math.floor(x / float(interval))) * interval
    else:
        return int(math.ceil(x / float(interval))) * interval


class BeatTracker(object):
    """
    Tracks the BPM (tempo) and volume of the song currently playing, using audio sampled from the microphone.
    """

    def __init__(self):
        self.tempo = 120
        self.last_tempo = 120
        self.volume = 1000
        self.sample_rate = 44100 / 2
        self.running = True
        self.thread = threading.Thread(target=self._start, args=())
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=1,
                                   rate=self.sample_rate,
                                   input=True)

    def _start(self):

        buffer_size = self.sample_rate * 1
        hop_length = 512

        self.stream.start_stream()

        while self.running:
            data = self.stream.read(buffer_size, exception_on_overflow=False)
            y = numpy.frombuffer(data, dtype=numpy.int16).astype(numpy.float)
            tempo, _ = librosa.beat.beat_track(y=y,
                                               start_bpm=120,
                                               tightness=100,
                                               sr=self.sample_rate,
                                               hop_length=hop_length)
            if tempo < 1:
                tempo = 1

            self.last_tempo = self.tempo
            self.tempo = float(roundup(tempo, interval=10))

            rms = librosa.feature.rmse(y=y, hop_length=self.sample_rate, frame_length=self.sample_rate)
            rms_avg = int(numpy.average(rms))
            self.volume = rms_avg
            print("[tracker] %s: %s" % (int(self.tempo), rms_avg))

        self.stream.close()

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
