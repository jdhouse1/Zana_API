import docxtpl
import flask
import convertapi
import yagmail
from flask import request
from flask_httpauth import HTTPBasicAuth
from passlib.context import CryptContext
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
app = flask.Flask(__name__)
auth = HTTPBasicAuth()
pwd_context = CryptContext(schemes=['sha512_crypt'])
my_email = 'Zana.Packing.API@gmail.com'
recipient_email = my_email
path = Path()
convertapi.api_secret = os.environ['CONVERTAPI_SECRET']
password_hash = os.environ['AUTH_HASH']


def send_email(order_number, body, attachments):
    yag = yagmail.SMTP(my_email)
    yag.send(
        to=recipient_email,
        subject=f"Order {order_number} from Zana",
        contents=body,
        attachments=attachments,
        cc='jdhouse1@asu.edu'
    )


@auth.verify_password
def verify_password(username, password):
    if pwd_context.verify(password, password_hash):
        return username


@app.route('/', methods=['GET'])
def home():
    return "Hello! - JD House"


@app.route('/v1/packing_slip/', methods=['POST'])
@auth.login_required
def packing_slip():
    necessary_keys = {'order_number',
                      'items',
                      'date',
                      'shipping_address',
                      'message',
                      }
    context = request.json
    if not necessary_keys <= context.keys():
        return f"Error - didn't receive correct arguments. The following arguments are required: {necessary_keys}"
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
@auth.login_required
def register_account():
    registration = request.json
    yagmail.register(**registration)
    return "Success!"


if __name__ == '__main__':
    app.run()
