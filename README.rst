ereturns
========

This portal is used for uploading and downloading data.

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

For local development:

::

  $ docker-compose -f local.yml up --build

For production:

::

  $ docker-compose -f production.yml up --build

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy ereturns

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd ereturns
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

