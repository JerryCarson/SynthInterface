import numpy as np
from scipy import signal
import pyofdm.codec

#there are some functions for signal genration
#they return array of Y values

def step(app):  #special function for frequency setup
    fr = int(float(app.getOptionBox("Частота (MHz)"))*(10**6))
    step = int(512/(100*(10**6)/fr)+0.5)
    return step

def sine(app):
    with open("input.txt", "w+") as input:
        a = np.linspace(0, 2*np.pi, 512)
        for i in range (0, 512, step(app)):
            input.write(str(np.sin(a[i]))) 
            input.write("\n")

def square(app):
    with open("input.txt", "w+") as input:
        t = np.linspace(0, 1, 512, endpoint=False)
        a = signal.square(2 * np.pi * 1 * t)
        for i in range (0, 512, step(app)):
            input.write(str(a[i]))
            input.write("\n")

def ofdm(freqSamples, carriers, order, dist, app):
    with open("input.txt", "w+") as input:

        a = app.getTextArea("t2").split()
        tx_im = np.array([a[i] for i in range(0, len(a))])
        tx_enc = np.array(tx_im, dtype="uint8").flatten()

        totalFreqSamples = int(freqSamples)
        sym_slots = int(carriers)
        QAMorder = int(order)
        nbytes = sym_slots*QAMorder//8

        distanceOfPilots = int(dist)
        pilotlist = pyofdm.codec.setpilotindex(nbytes,QAMorder,distanceOfPilots)

        ofdm = pyofdm.codec.OFDM(pilotAmplitude = 1,
                                nData=nbytes,
                                pilotIndices = pilotlist,
                                mQAM = QAMorder,
                                nFreqSamples = totalFreqSamples)

        tx_enc = np.append(tx_enc,np.zeros((sym_slots-tx_enc.size)%sym_slots, dtype="uint8"))

        complex_signal = np.array([ofdm.encode(tx_enc[i:i+nbytes]) for i in range(0,tx_enc.size,nbytes)]).ravel()

        for i in range (0, complex_signal.size):
                input.write(str(float(complex_signal[i])))
                input.write("\n")
