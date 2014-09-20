"""
Test the server, requires that the server is already running.
"""
import os
import requests
import base64
import unittest


class PDFAPITestCase(unittest.TestCase):
    server_url = 'http://localhost:5000/'

    def test_status(self):
        r = requests.get(self.server_url)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json(), {u'status': u'no idea', u'system': u'PDF generation API'})

    def test_example(self):
        r = requests.get(self.server_url + 'example')
        self.assertEqual(r.status_code, 200, r.text)
        pdf_content = base64.b64decode(r.text)
        self.assertEqual(pdf_content[:4], '%PDF')

    def test_create(self):
        html = '<div align="center"><h1>This is a test!</h1></div>'
        r = requests.post(self.server_url + 'create', data={'html': html})
        self.assertEqual(r.status_code, 200, r.text)
        pdf_content = base64.b64decode(r.text)
        self.assertEqual(pdf_content[:4], '%PDF')

    def test_create2(self):
        this_dir = os.path.dirname(__file__)
        html_file = os.path.join(this_dir, 'test.html')
        html = open(html_file, 'r').read()
        get_args = '?copies=3&margin_left=30mm&margin_right=30mm'
        r = requests.post(self.server_url + 'create' + get_args, data={'html': html})
        self.assertEqual(r.status_code, 200, r.text)
        pdf_content = base64.b64decode(r.text)
        self.assertEqual(pdf_content[:4], '%PDF')
        # open('test.pdf', 'w').write(pdf_content)

if __name__ == '__main__':
    unittest.main()
