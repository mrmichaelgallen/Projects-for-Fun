#!/usr/bin/env python

# This uses the pyaudio library for sound playback
# https://people.csail.mit.edu/hubert/pyaudio/
import pyaudio

import argparse
import random
import math

########################################
def parseArguments():
    parser = argparse.ArgumentParser(description="I play music")

    parser.add_argument('-bitwidth',
                        default=8,
                        type=int,
                        help="Bitwidth of the audio samples,  NOT IMPLEMENTED")

    parser.add_argument('-channels',
                        default=1,
                        type=int,
                        help="Number of audio channels (1=mono, 2=stereo),  NOT IMPLEMENTED")

    parser.add_argument('-rate',
                        default=48000,
                        type=int,
                        help="Sample rate (Hz)")


    return parser.parse_args()

########################################
# get the number of bytes per audio sample
def bytesPerSample(args):
    return int(args.bitwidth/8)

########################################
# generate randomNoise
def noise(duration, args):
    bufferLen = int(duration * args.rate)

    buffer = bytearray()
    for sample in range(bufferLen):
        buffer.append(random.randint(0, 255))
    return buffer

########################################
# generate a square wave
def squareWave(frequency, duration, args):
    bufferLen = int(duration * args.rate)

    period = int(args.rate / frequency)   # a low-high cycle consists of this many samples
    lowHighTransition = period / 2  # place where we transition low value -> high value

    buffer = bytearray()
    for sample in range(bufferLen):
        locationInCurrPeriod = sample % period
        if locationInCurrPeriod < lowHighTransition:
            buffer.append(0)
        else:
            buffer.append(255)
    return buffer

########################################
# generate a sinusoidal wave
def sineWave(frequency, duration, args):
    bufferLen = int(duration * args.rate)

    period = int(args.rate / frequency)   # a low-high cycle consists of this many samples

    buffer = bytearray()
    for sample in range(bufferLen):
        locationInCurrPeriod = sample % period
        val = math.sin(1.0 * locationInCurrPeriod / period * 2 * math.pi)  # -1..1
        clampedVal = int(255.0 * (val + 1) / 2);  # 0..255
        buffer.append(clampedVal)
    return buffer



########################################
def main():
    args = parseArguments()

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(bytesPerSample(args)),
                    channels=args.channels,
                    rate=args.rate,
                    output=True)

    # http://www.phy.mtu.edu/~suits/notefreqs.html
    noteToFrequency = {"A": 440,
                       "B": 494,
                       "C": 523,
                       "D": 587,
                       "E": 659,
                       "F": 698,
                       "G": 784};

    #data = noise(5, args)

    if 1:
        data = (squareWave(noteToFrequency["A"], 1, args)
                + squareWave(noteToFrequency["B"], 0.5, args)
                + squareWave(noteToFrequency["C"], 2, args))
    else:
        data = (sineWave(noteToFrequency["A"], 1, args)
                + sineWave(noteToFrequency["B"], 0.5, args)
                + sineWave(noteToFrequency["C"], 2, args))


    stream.write(bytes(data))

main()
