.. _installation_label:

Installation
============

**Hinweis: Nur Linux, Windows wird derzeit nicht unterstützt.**

Klonen Sie zunächst über SSH mit

.. code-block::

   git clone git@github.com:rl-institut-private/digipipe.git /local/path/to/digipipe/

Voraussetzung ist:

* `conda` (`Anaconda <https://docs.anaconda.com/anaconda/install/>`_ / `Miniconda <https://conda.io/en/latest/miniconda.html>`_)
* `python <https://www.python.org/downloads/>`_

Navigieren Sie in den Repo-Ordner. Richten Sie eine conda-Umgebung ein und aktivieren Sie sie mit:

.. code-block::

   conda env create -f environment.yml
   conda activate digiplan

Installieren Sie `poetry <https://python-poetry.org/>`_ (der in diesem Projekt verwendete Python-Abhängigkeitsmanager
Projekt) und Abhängigkeiten für das Projekt (Hinweis: Die Installation von poetry via pip in dieselbe Umgebung wird
nicht empfohlen und kann Probleme verursachen! Stattdessen sollte es systemweit über den unten stehenden Befehl oder
`pipx <https://python-poetry.org/docs/#installing-with-pipx>`_ installiert werden):

.. code-block::

   curl -sSL https://install.python-poetry.org | python3 -
   poetry install

Es werden einige zusätzliche Systempakete benötigt, die Sie mit dem folgenden Befehl installieren

.. code-block::

   apt install gdal-bin python3-gdal libspatialindex-dev imagemagick osmium-tool graphviz graphviz-dev

Weitere Anmerkungen:

* Stellen Sie sicher, dass Sie `GDAL>=3.0` haben, da ältere Versionen nicht funktionieren.
* `imagemagick` ist optional und nur für die Berichtserstellung erforderlich
