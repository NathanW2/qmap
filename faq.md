---
layout: empty
title: FAQ
---

### Why QGIS?

Why not? 

### What data formats does QMap support?

Anything QGIS supports QMap does as well. QMap is just QGIS with a interface that is easier to use for field based data collection.

### Does QMap support online or offline maps?

Both.  QMap is just QGIS. If you would like a fully offline system you can just have local files, local SpataiLite, local PostGIS/MS SQL 2008+ install, etc.  If you want a online system with a WMS base just create a project with a WMS layer. 

### What about forms. Will QMap auto generate forms for me?

Currently no.  Forms must be built with Qt Designer (installed with qt4-deval from OSGeo4W).  Auto forms were considered but for now having control over the layout of the forms was more important.  Auto forms could be generated using the method QGIS does if needed.  Feel free to open a issue if you think it is needed.

### Y U No Support Android? 

;) Hopefully once we have Python support for QGIS Android I can start working on a version for Android but for now this is really designed for Windows based tablets.  We use Motion F5Vs, but anything that runs Windows will work fine.

### What version of QGIS do I need?

For QMap to work correctly you need to be running the latest development build, sorry about that. There are a few bugs in 1.8 that I fixed in order to get QMap to run the way it should.

### Is MS SQL 2008 Syncing required?

Not at all. You can build the project with --with-mssyncing=False to disable SQL 2008 syncing.  We only have this because we store all our data on the clients in a local MS SQL 2008 database.  

### What about syncing support for other file formats?

Sorry not yet.  PostGIS and SpatiaLite syncing support would be nice to have in the future.  [GeoGit](https://github.com/opengeo/GeoGit) also looks promising but is not ready yet.

