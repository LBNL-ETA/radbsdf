.. radbsdf documentation master file, created by
   sphinx-quickstart on Tue Sep  7 14:45:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to radbsdf's documentation!
===================================

radbsdf is an Python wrapper for the Radiance BSDF library.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

User Guide
----------

A user can use radbsdf to read and analyze BSDF.

To load a tabular BSDF (.xml) file:

.. code-block::

   import radbsdf
   sd_data = radbsdf.TabularBSDF("venetian_blinds.xml")

Once the BSDF is loaded, one can check BSDF summary:

.. code-block::

   sd_data.get_summary()

An summary will be printed out::

   Materials: VBlinds
   Manufacturer: Manufacturer
   Width, Height, Thickness (m): 0.0 0.0 0.0
   Peak front hemispherical transmittance: 0.026940606546542577
   Peak back hemispherical transmittance: 0.029215388356407145
   Peak front hemispherical reflectance: 0.1651114347940009
   Peak back hemispherical reflectance: 0.16018741824894725
   Diffuse Front Reflectance: 0.05820334271141809 0.05820334271141809 0.05820333924222852
   Diffuse Back Reflectance: 0.052836873507863834 0.052836873507863834 0.05283687035854076
   Diffuse Front Transmittance: 0.0 0.0 0.0
   Diffuse Back Transmittance: 0.0 0.0 0.0


One can further examine direct hemispherical results for a given angle of incidence. Before we do that, we need to transform our coordinate systems to cartesian:

.. code-block::

   tin = 30
   pin = 270
   theta = math.radians(tin)
   phi = math.radians(pin)
   x = math.sin(theta) * math.cos(phi)
   y = math.sin(theta) * math.sin(phi)
   z = math.cos(theta)
   ivec = [x, y, z]

Once we have our angle of incidence in cartesian coordinate, we can obtain various hemispherical results like so:

.. code-block::

   hemis_scattering = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
   hemis_transmittance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
   hemis_reflectance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rh"])
   hemis_specular_transmittance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Ts"])
   hemis_diffuse_transmittance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Td"])
   hemis_specular_reflectance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rs"])
   hemis_diffuse_reflectance = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rd"])

We can also query the BSDFF given a pair of incience and exiting angle. The outgoing angle needs also to be in cartesian coordiate:

.. code-block::

   sd_data.query(ovec, ivec)

In addition, we can also query the projected solid angle for a given angle of incience:

.. code-block::

   sd_data.proj_solid_angle(ivec)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
