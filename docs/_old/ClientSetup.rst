======================
|name| - Client Setup
======================

.. |name| replace:: QMap
.. |f| image:: images/folder.png

.. contents::
.. sectnum::

Installing QGIS
=======================

Installing MS SQL
=======================

SQL Express can be installed on the client by running `client-setup/install-sql.bat`

Installing |name|
=======================

Provisioning MS SQL Tables
==========================

geometry_columns and spatial_ref_sys must be created on the client in order for
QGIS to open the tables correctly.

Create geometry_columns table

.. code:: sql

    USE [FieldData]
    GO

    /****** Object:  Table [dbo].[geometry_columns]    Script Date: 07/11/2012 09:36:44 ******/
    SET ANSI_NULLS ON
    GO

    SET QUOTED_IDENTIFIER ON
    GO

    SET ANSI_PADDING ON
    GO

    CREATE TABLE [dbo].[geometry_columns](
        [f_table_catalog] [varchar](128) NOT NULL,
        [f_table_schema] [varchar](128) NOT NULL,
        [f_table_name] [varchar](256) NOT NULL,
        [f_geometry_column] [varchar](256) NOT NULL,
        [coord_dimension] [int] NOT NULL,
        [srid] [int] NOT NULL,
        [geometry_type] [varchar](30) NOT NULL,
     CONSTRAINT [geometry_columns_pk] PRIMARY KEY CLUSTERED
    (
        [f_table_catalog] ASC,
        [f_table_schema] ASC,
        [f_table_name] ASC,
        [f_geometry_column] ASC
    )WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
    ) ON [PRIMARY]

    GO

    SET ANSI_PADDING OFF
    GO

Create spatial_ref_sys table

.. code:: sql

    USE [FieldData]
    GO

    /****** Object:  Table [dbo].[spatial_ref_sys]    Script Date: 07/11/2012 09:37:41 ******/
    SET ANSI_NULLS ON
    GO

    SET QUOTED_IDENTIFIER ON
    GO

    SET ANSI_PADDING ON
    GO

    CREATE TABLE [dbo].[spatial_ref_sys](
        [srid] [int] NOT NULL,
        [auth_name] [varchar](256) NULL,
        [auth_srid] [int] NULL,
        [srtext] [varchar](2048) NULL,
        [proj4text] [varchar](2048) NULL,
    PRIMARY KEY CLUSTERED
    (
        [srid] ASC
    )WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
    ) ON [PRIMARY]

    GO

    SET ANSI_PADDING OFF
    GO
