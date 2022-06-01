import numpy as np
from scipy import signal
import pyofdm.codec
import pyofdm.nyquistmodem

k=200 #какое-то опорное число, задается пользователем

def sine(app):
    with open("input.txt", "w+") as input:
        a = np.linspace(0, 2*np.pi, k*16) #одномерный массив значений икса (старт, стоп, количество точек между)
        for i in range (0, k*16):
            input.write(str(np.sin(a[i]))) #генерируем значения синуса на основе массива иксов
            input.write("\n")

def square(app): #то же самое для прямоугольного импульса
    with open("input.txt", "w+") as input:
        t = np.linspace(0, 1, k*16, endpoint=False)
        a = signal.square(2 * np.pi * 1 * t)
        for i in range (0, k*16):
            input.write(str(a[i]))
            input.write("\n")

def ofdm(freqSamples, carriers, order, dist, app):
    with open("input.txt", "w+") as input:
        # tx_im = np.array([], dtype=int)
        a = app.getTextArea("t2").split()
        tx_im = np.array([a[i] for i in range(0, len(a))])
        # for i in range (0, len(a)):
        #     np.append(tx_im, a[i])
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



