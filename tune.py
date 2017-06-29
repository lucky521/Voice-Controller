import wave
import numpy
import sys
import matplotlib
import matplotlib.pyplot as plt
#########################################################################
# Matplotlib
def show_fft(fft_data, fft_data2):
    fig, ax = plt.subplots(2,1)
    ax[0].plot(fft_data)
    ax[1].plot(fft_data2)
    plt.show()
    return

#########################################################################
# Tuning functions

def tune(data, ratio):
    fft_data = numpy.fft.rfft(data)
    #new_fft = [fft_data[(round(i/float(ratio)))%len(fft_data)] for i in xrange(len(fft_data))]
    new_fft = []
    for i in xrange(len(fft_data)):
        new_fft.append(fft_data[(round(i/float(ratio)))%len(fft_data)])
    #print "len(data)",len(data),"len(fft_data)",len(fft_data),"len(new_fft)",len(new_fft)
    #show_fft(fft_data, new_fft)
    return numpy.fft.irfft(new_fft)

def tuneChannel(data, ratio):
    ret = []
    chunksize = wav.getframerate() / 8
    print "chunksize", chunksize
    for i in xrange(0, len(data), chunksize):
        chunk = data[i:i+chunksize]
        ret += list(tune(chunk, ratio))
    return ret

##########################################################################
# Filtering functions


##########################################################################
# Main process
if len(sys.argv) != 3:
    print "Usage: python tune.py test.wave 1.25"
    sys.exit()

# Open wav from wav file
wav_file = sys.argv[1]
wav = wave.open(wav_file)
print "wave.getsampwidth " + str(wav.getsampwidth())
print "wave.getnchannels " + str(wav.getnchannels()) # 1 for mono, 2 for stereo
print "wave.getframerate " + str(wav.getframerate())
print "wave.getnframes " + str(wav.getnframes())

# Format raw frames bytes to array
datatype = numpy.dtype('<i' + str(wav.getsampwidth()))
print "sample type", datatype
raw_data = numpy.fromstring(wav.readframes(wav.getnframes()), datatype)
print "total frames num: ", len(raw_data)

# Separate 2 channel to channels_data[i]
channels_data = [raw_data[i::wav.getnchannels()] for i in xrange(wav.getnchannels())]

# Do tune for each channel
for i in xrange(wav.getnchannels()):
    print "Frame num in channel ", i, " : ",len(channels_data[i]) 
    channels_data[i] = tuneChannel(channels_data[i], sys.argv[2])

# Merge 2 channel back to single stream
final_data = []
for j in xrange(len(channels_data[0])):
    for i in xrange(len(channels_data)):
            final_data += [channels_data[i][j]]
final_data = numpy.array(final_data, dtype=datatype).tostring()

# Write wav to wav file
new_wav = wave.open('out.wav', 'w')
new_wav.setparams(wav.getparams())
new_wav.writeframes(final_data)
new_wav.close()

