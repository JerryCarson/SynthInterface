from appJar import gui 

app=gui("Grid Demo", "300x300")
app.setSticky("news")
app.setExpand("both")
app.setFont(14)

app.addLabel("l1", "row=0\ncolumn=0", 0, 0)
app.addLabel("l2", "row=0\ncolumn=1", 0, 2)
app.addLabel("l3", "row=0\ncolumn=0", 1, 0)
app.addLabel("l4", "row=0\ncolumn=1", 1, 2)
app.addVerticalSeparator(0, 1, 0, 2, colour="black")


app.setLabelBg("l1", "red")
app.setLabelBg("l2", "blue")

app.go()