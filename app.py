import docxtpl
import flask
import convertapi
import yagmail
from flask import request
from pathlib import Path
import os

app = flask.Flask(__name__)
x = ''
my_email = 'Zana.Packing.API@gmail.com'
recipient_email = my_email
path = Path()
convertapi.api_secret = os.environ['CONVERTAPI_SECRET']


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
    pdf = convertapi.convert('pdf', {'File': temp}, from_format='docx')
    pdf.save_files(name)
    body = ""
    send_email(context['order_number'], body, name)
    os.remove(name)
    return "Success!"


@app.route('/register/', methods=['POST'])
def register_account():
    registration = request.json
    yagmail.register(*registration)
    return "Success!"


if __name__ == '__main__':
    app.run()
