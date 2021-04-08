import docx2pdf
import docxtpl
import flask
import pythoncom
import yagmail
from flask import request
from pathlib import Path
import os

app = flask.Flask(__name__)
x = ''
my_email = 'Zana.Packing.API@gmail.com'
recipient_email = my_email
path = Path()


def send_email(order_number, body, attachments):
    yag = yagmail.SMTP(my_email)
    yag.send(
        to=recipient_email,
        subject=f"Order {order_number} from Zana",
        contents=body,
        attachments=attachments,
        cc='jdhouse1@asu.edu'
    )


@app.route('/', methods=['GET'])
def home():
    return "Hello! - JD House"


@app.route('/test/', methods=['POST'])
def test():
    print(request.form)
    print(dict(request.form))
    global x
    x += request.form['data']
    return "Success"


@app.route('/v1/packing_slip/', methods=['POST'])
def packing_slip():
    context = request.json
    name = path / f"Order_{context['order_number']}.pdf"
    temp = path / 'temp.docx'
    doc = docxtpl.DocxTemplate(path / 'packing_slip.docx')
    doc.render(context)
    doc.save(temp)
    pythoncom.CoInitialize()
    docx2pdf.convert(temp, name)
    body = ""
    send_email(context['order_number'], body, name)
    os.remove(name)
    return "Success!"


app.run()
