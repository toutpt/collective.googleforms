Introduction
============

Google provides a service which let you create forms_. This add-on let you display
a form from this service in your Plone site.

How it works
============

  * This add-on parse the html of the form you have built in google doc with beautifulsoup_.
  * It build a form with the same html markup as archetypes one, so the form seems to be a plone one.
  * The action is the google doc one, so you are redirected to it when submiting.

Credits
=======

Companies
---------

|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_


Authors

  - JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

Contributors

  -

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _forms: http://docs.google.com/support/bin/topic.py?topic=15166
.. _beautifulsoup: http://pypi.python.org/pypi/BeautifulSoup
