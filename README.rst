sbd - Cookies based version - A python tool to convert Safari Books Online resources into PDF.
==================================

Update hardcoded cookies into sbd.py than run it with link to Safari book as argument.

NB: This is a dirty quick modification.




This project fetches relevant data from Safari Books Online pages and generates a single pdf with the content.

Installation
------------

1. Install sbd with pip

.. code-block:: bash

	$ pip install sbd

2. Install `wkhtmltopdf`_

* Debian/Ubuntu:

.. code-block:: bash

	$ sudo apt-get install wkhtmltopdf

* Windows and other options: check wkhtmltopdf `homepage <http://wkhtmltopdf.org/>`_ for binary installers

.. _wkhtmltopdf: http://wkhtmltopdf.org/


Usage
-----
.. code-block:: bash

	$ usage: sbd [-h] safari_book_url

You need to export your cookies and update the script with correct values.

.. code-block:: bash

$ sbd https://learning.oreilly.com/library/view/linux-observability-with/9781492050193/






