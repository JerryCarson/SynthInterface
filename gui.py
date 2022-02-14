import ser
from appJar import gui

app = gui()
app.addFileEntry("f1")
app.addTextArea("t1")
app.addLabelEntry("COM port name")
app.addLabelEntry("Baud rate")


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        if app.getTextArea("t1") != "":
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