import numpy as np
import pyofdm.codec
import pyofdm.nyquistmodem
import matplotlib.pyplot as plt

# load the image
tx_im = np.array([34,62435,67,34567,2435,47,4257,24,2345,6732457,23457]) #Image.open('DC4_300x200.pgm')
# Npixels = tx_im.size[0]*tx_im.size[1]
tx_enc = np.array(tx_im, dtype="uint8").flatten()

# We do DVB-T 2k
# https://www.etsi.org/deliver/etsi_en/300700_300799/300744/01.06.01_60/en_300744v010601p.pdf

# Number of total frequency camples
totalFreqSamples = 2048

# Number of useful data carriers / frequency samples
sym_slots = 16

# QAM Order 
QAMorder = 8

# Total number of bytes per OFDM symbol
nbytes = sym_slots*QAMorder//8

# Distance of the evenly spaced pilots
distanceOfPilots = 12
pilotlist = pyofdm.codec.setpilotindex(nbytes,QAMorder,distanceOfPilots)

ofdm = pyofdm.codec.OFDM(pilotAmplitude = 1,
                         nData=nbytes,
                         pilotIndices = pilotlist,
                         mQAM = QAMorder,
                         nFreqSamples = totalFreqSamples)

# add zeros to make data a whole number of symbols
tx_enc = np.append(tx_enc,np.zeros((sym_slots-tx_enc.size)%sym_slots, dtype="uint8"))

complex_signal = np.array([ofdm.encode(tx_enc[i:i+nbytes]) for i in range(0,tx_enc.size,nbytes)]).ravel()

plt.plot(complex_signal)

# plt.title("OFDM complex spectrum")
# plt.xlabel("Normalised frequencies")
# plt.ylabel("Frequency amplitudes")
# plt.plot(np.linspace(0,1,len(complex_signal)),(1/len(complex_signal))*np.abs(np.fft.fft(complex_signal)))

# base_signal = pyofdm.nyquistmodem.mod(complex_signal)
# # save it as a wav file
# wav.write('ofdm44100.wav',44100,base_signal)

# plt.figure()
# plt.title("OFDM baseband spectrum after Nyquist modulation")
# plt.xlabel("Normalised frequencies")
# plt.ylabel("Frequency amplitudes")
# plt.plot(np.linspace(0,1,len(base_signal)),(1/len(base_signal))*np.abs(np.fft.fft(base_signal)))
plt.show()
