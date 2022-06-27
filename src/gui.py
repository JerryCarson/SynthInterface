from msilib.schema import RadioButton
import port as port
import numpy as np
from appJar import gui
import os
import signal_presets
from matplotlib.ticker import EngFormatter
import tooltip_list
import inits

app = gui("Serial Communication")
app.setResizable(canResize=False)

def checkStop():
    f.close()
    f1.close()
    if os.path.exists(inits.IN):
        os.remove(inits.IN)
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    return app


def getXY():
    y = []
    with open("output.txt", "r") as input:
        for line in input:
            if (line != "\n") and (not(line.isspace())):
                y.append(float(line))
    x = np.arange(0.0, np.size(y)*10, 10)
    return x, y


def showLabels():
    axes.set_xlabel("Время (нс)")
    axes.set_ylabel("Амплитуда")
    formatter1 = EngFormatter(places=1, sep="\N{THIN SPACE}")
    axes.xaxis.set_major_formatter(formatter1)
    app.refreshPlot("p1")


def press(button):

    COM = app.getEntry("COM порт")
    SAMPL = app.getEntry("Семплы")
    CAR_NUM = app.getEntry("Число поднесущих")
    ORDER = app.getOptionBox("Размер созвездия")
    DIST = app.getEntry("Расстояние между пилот-несущими")
    mu = app.getEntry("Значение:")
    sigma = app.getEntry("Стандартное отклонение:")

    if button == "Начать генерацию":
        handler = port.SerialWrite(COM, inits.BR, inits.IN, app)
        handler.generationStart()
    elif button == "Остановить":
        handler = port.SerialWrite(COM, inits.BR, inits.IN, app)
        handler.generationStop()
    elif button == "Формировать сигнал":
        if app.getTabbedFrameSelectedTab("TabbedFrame") == "Простые сигналы":
            if app.getTabbedFrameSelectedTab("1") == "Текстовое поле":
                c = port.SerialWrite(COM, inits.BR, inits.IN, app)
                c.comWriteField()
            elif app.getTabbedFrameSelectedTab("1") == "Файл с отсчетами":
                c = port.SerialWrite(COM, inits.BR, app.getEntry("f1"), app)
                c.comWrite()
            elif app.getTabbedFrameSelectedTab("1") == "Готовые шаблоны":
                if app.getOptionBox("Шаблон") == "Синус":
                    signal_presets.sine(app)
                elif app.getOptionBox("Шаблон") == "Прямоугольный импульс":
                    signal_presets.square(app)
                elif app.getOptionBox("Шаблон") == "Случайный сигнал по Гауссу":
                    signal_presets.gauss(mu, sigma, app)
                c = port.SerialWrite(COM, inits.BR, inits.IN, app)
                c.comWrite()
        elif app.getTabbedFrameSelectedTab("TabbedFrame") == "OFDM генерация":
            if app.getRadioButton("song") == "Формировать огибающую":
                signal_presets.ofdm(SAMPL, CAR_NUM, ORDER, DIST, app)
                c = port.SerialWrite(COM, inits.BR, inits.IN, app)
                c.comWrite()
            elif app.getRadioButton("song") == "Формировать сигнал":
                signal_presets.get_envelope(signal_presets.ofdm(
                    SAMPL, CAR_NUM, ORDER, DIST, app), app)
                c = port.SerialWrite(COM, inits.BR, inits.IN, app)
                c.comWrite()

        axes = app.updatePlot("p1", *getXY())
        showLabels()


def opt_changed():
    if app.getOptionBox("Шаблон") == "Случайный сигнал по Гауссу":
        app.showLabel("Значение:")
        app.showLabel("Стандартное отклонение:")
    else:
        app.hideLabel("Значение:")
        app.hideLabel("Стандартное отклонение:")


app.startTabbedFrame("TabbedFrame")
app.startTab("Простые сигналы")

app.setExpand("both")

app.startTabbedFrame("1")
app.startTab("Файл с отсчетами")
app.addFileEntry("f1")
app.stopTab()

app.startTab("Готовые шаблоны")
app.addLabelOptionBox("Шаблон", inits.SAMPLS)
app.addLabelOptionBox("Частота (МГц)", inits.FRQS)
app.addLabelEntry("Значение:")
app.setEntry("Значение:", 0)
app.addLabelEntry("Стандартное отклонение:")
app.setEntry("Стандартное отклонение:", 10)
app.hideLabel("Значение:")
app.hideLabel("Стандартное отклонение:")
app.setOptionBoxChangeFunction("Шаблон", opt_changed)
app.stopTab()

app.startTab("Текстовое поле")
app.addTextArea("t1")
app.setTextArea("t1", "1\n2\n1\n2\n1\n")
app.stopTab()

app.stopTabbedFrame()

app.setStopFunction(checkStop)

app.stopTab()

app.startTab("OFDM генерация")

app.setExpand("both")
app.addTextArea("t2")
app.addRadioButton("song", "Формировать сигнал")
app.addRadioButton("song", "Формировать огибающую")
app.addLabelEntry("Семплы")
app.addLabelEntry("Число поднесущих")
app.addLabelOptionBox("Размер созвездия", [2, 4, 8])
app.addLabelEntry("Расстояние между пилот-несущими")
app.setEntry("Семплы", 2048)
app.setEntry("Число поднесущих", 16)
app.setEntry("Расстояние между пилот-несущими", 12)
app.setTextArea("t2", "1\n2\n3\n4\n5\n")

app.stopTab()
app.stopTabbedFrame()

app.addVerticalSeparator(0, 1, 0, 12, colour="black")
app.addHorizontalSeparator(colour="black")
app.addLabelEntry("COM порт")
app.setEntry("COM порт", "COM1")
app.addHorizontalSeparator(colour="black")
app.addButtons(["Формировать сигнал", "Начать генерацию",
               "Остановить"], press, 10, 0)
app.addWebLink("GitHub (исходный код)",
               "https://github.com/JerryCarson/SynthInterface")

f = open(inits.IN, "w+")
f1 = open("output.txt", "w+")
axes = app.addPlot("p1", *getXY(), 0, 2, 12, 12)
showLabels()

tooltip_list.set_tooltips(app)

app.go()
