import wave
import sys
import numpy

def show_data_statistic(data):
    print '##################'
    print 'channels_data', data
    print 'length', len(data)
    print 'type', type(data[0])
    print 'min', data.min()
    print 'max', data.max()
    print 'mean', data.mean()
    print 'median', numpy.median(data)


# Main process
if len(sys.argv) != 3:
    print "Usage: python amplify.py test.wave 1.5"
    sys.exit()

wav_file = sys.argv[1]
scale = float(sys.argv[2])

# Open wav from wav file
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

show_data_statistic(channels_data[0])

# do amplify
channels_data[0] = numpy.int16(channels_data[0] * scale)
channels_data[1] = numpy.int16(channels_data[1] * scale)

show_data_statistic(channels_data[0])

# Merge 2 channel back to single stream
final_data = []
for j in xrange(len(channels_data[0])):
    for i in xrange(len(channels_data)):
            final_data += [channels_data[i][j]]
final_data = numpy.array(final_data, dtype=datatype).tostring()

# Write wav to wav file
new_wav = wave.open('amplified.wav', 'w')
new_wav.setparams(wav.getparams())
new_wav.writeframes(final_data)
new_wav.close()

