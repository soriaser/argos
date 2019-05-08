Argos
==========

Gaia statistics reader extension of [Argos](https://github.com/titusjan/argos).

### Installing Argos (with Gaia Extension)

Use same steps defined in [Argos](https://github.com/titusjan/argos) original project, but changing:

    %> pip install argos

by

    %> pip install argosge

Otherwise, original installation will be done (without extension).

### New in Argos Gaia Extension

* When loading Gaia GAT HDF5 statistics file, Argos (with extension) is able to preview healpix maps by using 'Matplotlib Healpix' inspector.
* It is possible to convert HDF5 Gaia GAT HDF5 statistic dataset into FITS by right clicking on dataset and chosing option 'To FITS'.
