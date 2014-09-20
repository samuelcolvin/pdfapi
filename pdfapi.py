import os
import traceback
import base64
from pydf import generate_pdf
from flask import Flask, jsonify, request

app = Flask(__name__)
IN_DOCKER = 'DOCKER' in os.environ


class RequestException(Exception):
    pass


def api_error(e, code=500):
    traceback.print_exc()
    return '%s: %s' % (e.__class__.__name__, str(e)), code


def safe_pdf(html, **kwargs):
    """
    Creates a base 64 encoded string representing a pdf which can safely
    be jsonified.
    """
    # Isn't there a more efficient way of doing this, which doesn't increase the
    # string length as much?
    pdf = generate_pdf(html, **kwargs)
    return base64.b64encode(pdf)


@app.route('/')
def status():
    """
    return message very simple pdf.
    """
    return jsonify(system='PDF generation API', status='no idea', docker=IN_DOCKER)


@app.route('/example')
def example():
    """
    generate a simple example.
    """
    ex = safe_pdf('<div align="center"><h1>PDF API</h1></div>')
    return ex, 200


@app.route('/create', methods=['POST'])
def create():
    """
    create a pdf from past data
    """
    try:
        data = request.form
        if len(data.keys()) == 1:
            key, value = data.items()[0]
            content = key if len(value) == 0 else value
        else:
            content = ''.join(v for v in data.values())
        kwargs = {k: v if len(v) > 1 else v[0] for k, v in request.args.items()}
        data = safe_pdf(content, **kwargs)
        return data
    except RequestException, e:
        return api_error(e, 400)


if __name__ == "__main__":
    host = '0.0.0.0' if IN_DOCKER else None
    app.run(host=host, debug=True, port=5000)
