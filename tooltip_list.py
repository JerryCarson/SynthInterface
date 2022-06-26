import ttps
def set_tooltips(app):
    app.setButtonTooltip("Формировать сигнал", ttps.buttonSIG)
    app.setButtonTooltip("Начать генерацию", ttps.buttonGEN)
    app.setButtonTooltip("Остановить", ttps.buttonSTOP)
    app.setEntryTooltip("COM порт", ttps.entryCOM)
    app.setTextAreaTooltip("t1", ttps.txt1)
    app.setTextAreaTooltip("t2", ttps.txt2)
    app.setEntryTooltip("f1", ttps.fileENTR)