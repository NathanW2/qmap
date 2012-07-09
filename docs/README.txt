====================
|name|
====================

:Authors:
    Nathan Woodrow,
    Damien Smith

:Version: 1.0

.. |name| replace:: QGIS Data Collector


.. contents::
.. sectnum::


The |name| is a simple to use, simple to configure, data collection
program built by Southern Downs Regional Council that uses QGIS.  |name| is a QGIS
Python plugin that removes most of the interface and replacing it with a simple
to use interface for data collection.

As |name| is just a Python plugin you can use your normal QGIS project files (.qgs)
in order to create mapping projects.

Requirements
-------------
- Latest QGIS Version > 1.8
- nose and mock (for Python tests)
- MS SQL Server 2008 (express or greater)
- .NET 3.5 (or greater)
- Microsoft Sync Framework
- Qt Designer (for form building)
- Something to install it on (some kind of fancy tablet PC)

Building
----------

For building we use fabricate_ which is a build tool written in pure Python,
because frankly GNUMake is a pain to use, the syntax is just plain strange,
and it sucks at error reporting.

.. _fabricate: http://code.google.com/p/fabricate/

To build just run **make_win.bat** from the main root folder.  build.py will generate
all the needed files and deploy them into the build directory.

The QGIS plugin location is /SDRCDataCollection/app/python/plugins

You can run build.py using Python:

.. code-block:: console

    #Clean build files
    python build.py clean

    #Build only docs
    python build.py docs
     
    #Build only
    python build.py build

The version number used is {year}.{month}.{day}.{commitid} and the version in
metadata.txt is the version number for all the files and related binaries in the
project.

Installing
----------

.. note:: If you haven't done so already please see Building_ before
          installing

Install the following software onto the client

    - MS SQL Server 2008
    - .NET 3.5
    - Microsoft Sync Framework
    - QGIS

Running the build.py file will compile and deploy the plugin to the list of
clients.

.. code-block:: console

    python build.py

The list of clients can be found in the function deploy_to_clients() inside
build.py.  Edit this list to add/remove clients.

.. note:: The build script will run the unit tests.  If any tests fail the
          build script will error and exit.  This is to prevent deploying a
          version that breaks already working code.

Conventions
-----------

|name| follows a convention over configuration style in order to
make setup consistant and easy. At times we still will need to configure things
but this will be kept to a minimum.

Form Conventions
++++++++++++++++

- Layer field names map to object names in Qt form (.ui)

  The form binder searchs the form for a widget named the same as the field and
  will bind and unbind the value from the layer to the form.  The widget type
  defines how the object is bound e.g. a column named *MyColumn* will bind
  to the QLineEdit::text() property of the widget with the same name.

  .. warning:: There is very little error handling with the form binding.
               Binding a char column with the value "Hello World" to a QCheckBox
               might do strange things.

- Date and time pickers can be created by placeing a button on the form with
  the same name as the DateTimeEdit control but with the *_pick* added to the name.

  .. figure:: DateTimePickerExample.png


  .. figure:: DateTimePickerExampleLayout.png

  Note the name of the QDateTimeEdit and the QPushButton.
  The QPushButton can live anywhere on the form, the only constraint is that it
  uses the {name}_pick convention.

  A correctly bound date time picker button has the word "Pick" and an icon.

  .. figure:: DateTimePickerBound.png

     Result of correct binding

- To correctly create a drawing pad button binding do the following:
    - Create a field in the datebase
    - Name a QPushButton with the field name - following the "fieldnames = object name"
      convention.
    - Label the button with "Drawing"

  .. figure:: DrawingBound.png

     Result of correct drawing button binding

  .. note:: The image is stored on the filesystem not in the layer. So no value is
           ever stored in the database. See `Program Conventions`_ for details on
           image convention.

- Adding a map picker button.  A tool that can be used to select a feature from
  the map can be added by adding a QToolButton to the form with the object name
  as {name}_mapselect where {name} is the name of the control the result will be
  bound to.

  .. figure:: MapSelectBound.png

     Control with QToolButton with the same name.

  In the above example the result of the map select will bind the result to the
  LotPlan control which is a QLineEdit.

  Two custom properties also need to be added to the buttom in order to define
  where the picked value comes from.

  The two properties are *from_layer* and *using_column*.

  .. figure:: MapSelectProperties.png

     Custom properties on QToolButton

  If any of the above properties are missing, or the layer supplied is not found,
  the map select button will be disabled.

  Adding custom properties will be explained in `Creating a new form`_

- Adding mandatroy fields. Fields that are mandatory will be highlighted, and
  if not filled in, will stop the user from leaving the form.

  To include a control as mandatory just add a "mandatory" bool custom property
  to the control that should be mandatory.

  .. figure:: MandatroyProperties.png

     Custom property to set mandatory flag.

  In order for the program to correctly handle highlighting the field as mandatory
  you also have to name the label for the control with {name}_label.  When the
  edit control is marked as mandatory its label will be highlighted.

  .. figure:: MandatoryLabelExample.png

Program Conventions
+++++++++++++++++++

- Images saved from drawing pad are stored in data\\{layername}\\images.
  Images have the following naming convention:

        {id}_{fieldname}.jpg

  Example:

        D896C1C0-9E4B-11E1-AB3F-002564CC69E0_Drawing.jpg

  Temp images that are saved before commit have the following convention and are
  saved in the user temp directory:

        drawingFor_{fieldname}.jpg

  *drawingFor\_* is replaced with *{id}* when the record is commited into the layer.
  The image is then moved into the images folder.

- Projects are stored in the projects\\ directory.  The name of the .qgs file will
  be used in the open project dialog box.  The project directory is **not** recursive

SQL Table Conventions
+++++++++++++++++++++
In order for syncing to be correctly setup the table must contain the following
columns:

    UniqueID as uniqueidentifier

    Primary Key column **must** be Int

Creating a new form
-------------------