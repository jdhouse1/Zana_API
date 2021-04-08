import docx2pdf
import docxtpl


def get_packing_slip(**kwargs):
    doc = docxtpl.DocxTemplate('packing_slip.docx')
    doc.render(kwargs)
    doc.save('temp.docx')
    docx2pdf.convert('temp.docx', 'output.pdf')


if __name__ == '__main__':
    print("hello")
    test_contents = [
        {'qty': 6, 'desc': 'Imprinted Z Sonics'},
    ]
    context = {
        'date': 'today',
        'order_number': 123,
        'shipping_address': '10615 N 44 St',
        'items': test_contents,
        'message': "success?",
    }
    get_packing_slip(**context)
