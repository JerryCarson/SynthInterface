from faulthandler import disable
from msilib.schema import RadioButton
import port as port
import numpy as np
from appJar import gui
import os
import signal_presets
from matplotlib.ticker import EngFormatter

app = gui("Serial Communication")

IN = "input.txt"
BR = 9600
FRQS = ["0.1953", "0.2016", "0.2083", "0.2155", "0.2232", "0.2315", "0.2404", "0.25", "0.2604", "0.2717", "0.2841", "0.2976", "0.3125", "0.3289",
        "0.3472", "0.3676", "0.3906", "0.4167", "0.4464", "0.4808", "0.5208", "0.5682", "0.625", "0.6944", "0.7813", "0.8929", "1.042", "1.25", "1.563", "2.083", "3.125", "6.25"]
SAMPLS = ["Синус", "Прямоугольный импульс"]


def pressRB(rb):
    if app.getRadioButton("ft") != "Готовые шаблоны:":
        app.disableOptionBox("Шаблон")
        app.disableOptionBox("Частота (МГц)")
    else:
        app.enableOptionBox("Шаблон")
        app.enableOptionBox("Частота (МГц)")


def checkStop():
    f.close()
    f1.close()
    if os.path.exists(IN):
        os.remove(IN)
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

    if button == "Начать генерацию":
        handler = port.SerialWrite(COM, BR, IN, app)
        handler.generationStart()
    elif button == "Остановить":
        handler = port.SerialWrite(COM, BR, IN, app)
        handler.generationStop()
    elif button == "Формировать сигнал":
        if app.getTabbedFrameSelectedTab("TabbedFrame") == "Простые сигналы":
            if app.getRadioButton("ft") == "Задать вручную в текстовом поле:":
                c = port.SerialWrite(COM, BR, IN, app)
                c.comWriteField()
            elif app.getRadioButton("ft") == "Файл с отсчетами":
                c = port.SerialWrite(COM, BR, app.getEntry("f1"), app)
                c.comWrite()
            elif app.getRadioButton("ft") == "Готовые шаблоны:":
                if app.getOptionBox("Шаблон") == "Синус":
                    signal_presets.sine(app)
                elif app.getOptionBox("Шаблон") == "Прямоугольный импульс":
                    signal_presets.square(app)
                c = port.SerialWrite(COM, BR, IN, app)
                c.comWrite()
        elif app.getTabbedFrameSelectedTab("TabbedFrame") == "OFDM генерация":
            if app.getRadioButton("song") == "Формировать огибающую":
                signal_presets.ofdm(SAMPL, CAR_NUM, ORDER, DIST, app)
                c = port.SerialWrite(COM, BR, IN, app)
                c.comWrite()
            elif app.getRadioButton("song") == "Формировать сигнал":
                signal_presets.get_envelope(signal_presets.ofdm(
                    SAMPL, CAR_NUM, ORDER, DIST, app), app)
                c = port.SerialWrite(COM, BR, IN, app)
                c.comWrite()

        axes = app.updatePlot("p1", *getXY())
        showLabels()


app.startTabbedFrame("TabbedFrame")
app.startTab("Простые сигналы")

app.setExpand("both")
app.addRadioButton(
    "ft", "Файл с отсчетами")
app.addFileEntry("f1")
app.addRadioButton("ft", "Готовые шаблоны:")
app.addLabelOptionBox("Шаблон", SAMPLS)
app.addLabelOptionBox("Частота (МГц)", FRQS)
app.addRadioButton("ft", "Задать вручную в текстовом поле:")
app.addTextArea("t1")
app.setTextArea("t1", "1\n2\n1\n2\n1\n")
app.disableOptionBox("Шаблон")
app.disableOptionBox("Частота (МГц)")
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

f = open(IN, "w+")
f1 = open("output.txt", "w+")
axes = app.addPlot("p1", *getXY(), 0, 2, 12, 12)
showLabels()

app.setButtonTooltip(
    "Формировать сигнал", "По нажатию кнопки данные сигнала загружаются на плату")
app.setButtonTooltip(
    "Начать генерацию", "По нажатию кнопки на плату отправляется команда - начать непрерывную генерацию заданного сигнала")
app.setButtonTooltip(
    "Остановить", "Отправляет на плату команду остановить генерацию сигнала")
app.setEntryTooltip(
    "COM порт", "Необходимо посмотреть номер порта, соответствующего подключенной плате. Доступные порты можно посмотреть в диспетчере устройств (выполнить compmgmt.msc)")

app.go()
