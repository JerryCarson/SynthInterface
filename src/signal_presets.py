import numpy as np
from scipy import signal
from scipy.signal import hilbert
import pyofdm.codec
import random

#there are some functions for signal genration
#they return array of Y values


def step(app):  #special function for frequency setup
    fr = int(float(app.getOptionBox("Частота (МГц)"))*(10**6))
    step = int(512/(100*(10**6)/fr)+0.5)
    return step

def sine(app):
    with open("input.txt", "w+") as input:
        a = np.linspace(0, 2*np.pi, 511)
        for i in range (0, 511, step(app)):
            input.write(str(np.sin(a[i]))) 
            input.write("\n")

def square(app):
    with open("input.txt", "w+") as input:
        t = np.linspace(0, 1, 511, endpoint=False)
        a = signal.square(2 * np.pi * 1 * t)
        for i in range (0, 511, step(app)):
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
    return complex_signal

def get_envelope(ofdm_signal, app):
    analytic_signal = (np.real(ofdm(app.getEntry("Семплы"), app.getEntry("Число поднесущих"), app.getOptionBox("Размер созвездия"), app.getEntry("Расстояние между пилот-несущими"), app)))
    with open('input.txt', 'w') as ouf:
        for i in range (0, analytic_signal.size):
            for j in range (0, 1):
                ouf.write(str(np.sin(i+j)*np.real(analytic_signal[i]+0.003)))
                ouf.write("\n")
    return np.abs(analytic_signal)

def gauss(mu, sigma, app):
    with open("input.txt", "w+") as input:
        a = np.empty(shape=(512), dtype=int)
        for i in range(0, 511):
            a[i] = random.gauss(0, 10)
        for i in range(0, 511, step(app)):
            input.write(str(a[i]))
            input.write("\n")
