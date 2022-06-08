from faulthandler import disable
import port as port
import numpy as np
from appJar import gui 
import os
import signal_presets

app = gui("Serial Communication")

def pressRB(rb):
    if app.getRadioButton("ft") != "Готовые шаблоны":
        app.disableOptionBox("Шаблон")
        app.disableOptionBox("Частота (MHz)")
    else:
        app.enableOptionBox("Шаблон")
        app.enableOptionBox("Частота (MHz)")

def checkStop():
    f.close()
    f1.close()
    if os.path.exists("input.txt"):
        os.remove("input.txt")
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    return app

def getXY():
    y = []
    with open("output.txt", "r") as input:
        for line in input:
            if (line != "\n") and (not(line.isspace())):
                y.append(float(line))
    x = np.arange(0.0, np.size(y))
    return x, y

def showLabels():
    axes.set_xlabel("Time")
    axes.set_ylabel("Amplitude")
    app.refreshPlot("p1")

def press(button):
    if button == "Начать генерацию":
        handler = port.SerialWrite(app.getEntry("COM порт"), app.getEntry("Baud rate"), "input.txt", app)
        handler.generationStart()
    elif button == "Остановить":
        handler = port.SerialWrite(app.getEntry("COM порт"), app.getEntry("Baud rate"), "input.txt", app)
        handler.generationStop()
    elif button == "Формировать сигнал":
        if app.getTabbedFrameSelectedTab("TabbedFrame") == "Simple signals":
            if app.getRadioButton("ft") == "Задать вручную в текстовом поле:":
                c = port.SerialWrite(
                    app.getEntry("COM порт"), app.getEntry(
                        "Baud rate"), "input.txt", app
                )
                c.comWriteField()
            elif app.getRadioButton("ft") == "Файл с отсчетами":
                c = port.SerialWrite(
                    app.getEntry("COM порт"),
                    app.getEntry("Baud rate"),
                    app.getEntry("f1"), app
                )
                c.comWrite()
            elif app.getRadioButton("ft") == "Готовые шаблоны":
                if app.getOptionBox("Шаблон") == "sin":
                    signal_presets.sine(app)
                elif app.getOptionBox("Шаблон") == "pulse":
                    signal_presets.square(app)
                c = port.SerialWrite(
                    app.getEntry("COM порт"),
                    app.getEntry("Baud rate"),
                    "input.txt", app
                )
                c.comWrite()
        elif app.getTabbedFrameSelectedTab("TabbedFrame") == "OFDM генерация":
            if app.getRadioButton("song") == "Формировать сигнал":
                signal_presets.ofdm(app.getEntry("Семплы"), app.getEntry("Число поднесущих"), app.getOptionBox("Размер созвездия"), app.getEntry("Расстояние между пилот-несущими"), app)
                c = port.SerialWrite(
                            app.getEntry("COM порт"),
                            app.getEntry("Baud rate"),
                            "input.txt", app
                        )
                c.comWrite()
            elif app.getRadioButton("song") == "Формировать огибающую":
                signal_presets.get_envelope(signal_presets.ofdm(app.getEntry("Семплы"), app.getEntry("Число поднесущих"), app.getOptionBox("Размер созвездия"), app.getEntry("Расстояние между пилот-несущими"), app), app)
                c = port.SerialWrite(
                            app.getEntry("COM порт"),
                            app.getEntry("Baud rate"),
                            "input.txt", app
                        )
                c.comWrite()

        axes = app.updatePlot("p1", *getXY())
        showLabels()

app.startTabbedFrame("TabbedFrame")
app.startTab("Simple signals")

app.setExpand("both")
app.addRadioButton("ft", "Файл с отсчетами")
app.addFileEntry("f1")
# app.addHorizontalSeparator(colour="black")
app.addRadioButton("ft", "Готовые шаблоны")
app.addLabelOptionBox("Шаблон", ["sin", "pulse"])
app.addLabelOptionBox("Частота (MHz)", ["0.1953", "0.2016", "0.2083", "0.2155", "0.2232", "0.2315", "0.2404", "0.25", "0.2604", "0.2717", "0.2841", "0.2976", "0.3125", "0.3289", "0.3472", "0.3676", "0.3906", "0.4167", "0.4464", "0.4808", "0.5208", "0.5682", "0.625", "0.6944", "0.7813", "0.8929", "1.042", "1.25", "1.563", "2.083", "3.125", "6.25"])
# app.addHorizontalSeparator(colour="black")
app.addRadioButton("ft", "Задать вручную в текстовом поле:")
# app.addLabelEntry("Частота", 5, 0)
app.addTextArea("t1")
app.setTextArea("t1", "1\n2\n1\n2\n1\n")
# app.addVerticalSeparator(0, 1, 0, 10, colour="black")
# app.setEntry("f1", "C://Users//1//Desktop/s.txt")
# app.setEntry("Частота", 1000)
app.disableOptionBox("Шаблон")
app.disableOptionBox("Частота (MHz)")
app.setRadioButtonChangeFunction("ft", pressRB)
app.setStopFunction(checkStop)

app.stopTab()

app.startTab("OFDM генерация")

app.setExpand("both")
app.addTextArea("t2")
app.addRadioButton("song", "Формировать сигнал")
app.addRadioButton("song", "Формировать огибающую")
app.addLabelEntry("Семплы")
app.addLabelEntry("Число поднесущих")
app.addLabelOptionBox("Размер созвездия", [2,4,8])
# app.addLabelEntry("Размер созвездия")
app.addLabelEntry("Расстояние между пилот-несущими")
app.setEntry("Семплы", 512)
app.setEntry("Число поднесущих", 16)
# app.setEntry("Размер созвездия", 8)
app.setEntry("Расстояние между пилот-несущими", 12)
app.setTextArea("t2", "1\n2\n3\n4\n5\n")

app.stopTab()
app.stopTabbedFrame()

app.addVerticalSeparator(0, 1, 0, 12, colour="black")
app.addHorizontalSeparator(colour="black")
app.addLabelEntry("COM порт")
app.addLabelEntry("Baud rate")
app.setEntry("COM порт", "COM1")
app.setEntry("Baud rate", 9600)
app.addHorizontalSeparator(colour="black")
app.addButtons(["Формировать сигнал", "Начать генерацию", "Остановить"], press, 10, 0)
# app.addMessage("")
app.addWebLink("GitHub", "https://github.com/JerryCarson/SynthInterface")

f = open("input.txt", "w+")
f1 = open("output.txt", "w+")
axes = app.addPlot("p1", *getXY(), 0, 2, 12, 12)
showLabels()
app.go()
