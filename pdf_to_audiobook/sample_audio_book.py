import PyPDF2
import pyttsx3

filename = "1.pdf"
with open(filename, "rb") as pdf_file:
    pdfreader = PyPDF2.PdfFileReader(pdf_file)
    speaker = pyttsx3.init()

    for page_num in range(pdfreader.numPages):
        print(page_num)
        text_obj = pdfreader.getPage(page_num)
        text = text_obj.extractText()
        print(text)
        rate = speaker.getProperty('rate')
        print(rate)
        voices = speaker.getProperty('voices')
        print(voices)
        # changing index, changes voices, 1 for female
        speaker.setProperty('voice', voices[1].id)
        speaker.setProperty('volume', 1.0)

        speaker.say(text)
        speaker.runAndWait()
    speaker.stop()
