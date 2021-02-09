Quickstart
==========

Get yourself up and running quickly.

Installation
------------

PyPI
~~~~
ValveFGD is available on the Python Package Index. This makes installing it with pip as easy as:

.. code-block:: bash

   pip3 install valvefgd

Git
~~~

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

.. code-block:: bash

   git clone git://github.com/pySourceSDK/ValveFGD.git

and install it from the repo directory with:

.. code-block:: bash

   python3 setup.py install

Usage
-----

Here's a few example usage of ValveFGD

Parsing
~~~~~~~

You can get a Fgd object by parsing an .fgd file using FgdParse

.. code-block:: python

   > from valvefgd import FgdParse

   > fgd = FgdParse('C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/bin/tf.fgd')

Writing
~~~~~~~

You can write an .fgd file from a Fgd object. It will write the fgd as it was parsed. The content of included Fgds will not be written unless you use the 'collapse' option.

.. note::
   Parsing/writing is destructive. Comments will be lost. The original structure of the file may be altered. The actual data about entities and the inheritance hierarchy is untouched however.

.. code-block:: python

   > from valvefgd import FgdWrite

   > FgdWrite(fgd, 'tf-clone.fgd')
   > FgdWrite(fgd, 'tf-clone.fgd', collapse=True)


Getting entity schemas
~~~~~~~~~~~~~~~~~~~~~~

You can get entity schematics from an Fgd object.

.. code-block:: python

   > env_fire = fgd.entity_by_name('env_fire')
   > print(env_fire.schema)

   {'properties': {'targetname': {'type': 'string', 'description': 'The name...'}, ...},
   'inputs': {'StartFire': {'type': 'void', 'description': 'Start the fire'}, ...},
   'outputs': {'onIgnited': {'type': 'void', 'description':'Fires when...'}, ...}}

Terminology
-----------
Here are some color coded charts for the terminology used in this library for fgd files.

FgdEntity
~~~~~~~~~
.. image:: /_static/fgdentity.jpg

FgdEntityInput/Output
~~~~~~~~~~~~~~~~~~~~~
.. image:: /_static/fgdentityio.jpg

FgdEntityProperty
~~~~~~~~~~~~~~~~~
.. image:: /_static/fgdentityproperty.jpg

FgdEntityPropertyOption
~~~~~~~~~~~~~~~~~~~~~~~
.. image:: /_static/fgdentitypropertyoption.jpg

FgdEntitySpawnflag
~~~~~~~~~~~~~~~~~~
.. image:: /_static/fgdentityspawnflags.jpg
