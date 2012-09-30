---
layout: doc
title: Getting Started
---

### Intro

QMap is a simple to use, simple to configure, data collection
program built by Southern Downs Regional Council that uses QGIS.  |name| is a QGIS
Python plugin that removes most of the interface and replacing it with a simple
to use interface for data collection.

Although this project is written as a QGIS plugin it is designed to be run 
in it's own QGIS sandbox using the --configpath command line option of QGIS. 
This means that it acts like a standalone program and will store its settings 
away from the normal QGIS install. This is to provide a controlled QGIS 
environment with a minimal interface

As QMAp is just QGIS with a new interface you can use your normal QGIS project files (.qgs)
in order to create mapping projects. Forms for each project are loaded based 
on the naming of layers in the project.  E.g. A form can be bound to the 
layer "Sewer Main" and will be useable in any project that includes 
a layer with the name "Sewer Main".

### Requirements

- Latest development QGIS Version (this is due to bug fixes in master)
- mock (for Python tests)
- Qt Designer (for form building)
- Something to install it on (some kind of fancy tablet PC)

If you want SQL Server syncing support

- MS SQL Server 2008 (express or greater)
- .NET 3.5 (or greater)
- Microsoft Sync Framework

OSGeo4W Packages

- qgis-dev
- qt4-devel

### Progam layout

