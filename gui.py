import ser
from appJar import gui

app = gui()
app.addRadioButton("ft", "Use file")
app.addRadioButton("ft", "Use text")
app.addFileEntry("f1")
app.addTextArea("t1")
app.addLabelEntry("COM port name")
app.addLabelEntry("Baud rate")
app.setEntry("COM port name", "COM1")
app.setEntry("Baud rate", 9600)
app.setEntry("f1", "C://Users//1//Desktop/s.txt")


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        if app.getRadioButton("ft") == "Use text":
            with open("input.txt", "w") as input:
                for line in app.getTextArea("t1"):
                    input.write(line)
            c = ser.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                "input.txt",
            )
            c.comWrite()
        else:
            c = ser.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                app.getEntry("f1"),
            )
            c.comWrite()


app.addButtons(["Submit", "Cancel"], press)

app.go()
