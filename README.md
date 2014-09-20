pdfapi
======

PDF API using docker.

This is very much a proof of concept, it uses flask not django and does the PDF generation in request-response
loop not on a worker.

To build docker image:

    docker build -t pdfapi .

To run it

    docker run -d -p 5000:5000 pdfapi

You can then test it with `servertest.py`.
