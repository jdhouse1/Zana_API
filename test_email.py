import yagmail

my_email = 'Zana.Packing.API@gmail.com'
yag = yagmail.SMTP(my_email)
print(yag)
receiver = my_email
body = "test"

yag.send(
    to=receiver,
    subject='test',
    contents=body,
)
