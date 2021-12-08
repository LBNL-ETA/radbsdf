#cython: language_level=3

cimport radbsdf
from cpython cimport array
import array

SFLAGS = {}
SFLAGS["Sh"] = radbsdf.SDsampAll
SFLAGS["Th"] = radbsdf.SDsampAll & ~radbsdf.SDsampR
SFLAGS["Rh"] = radbsdf.SDsampAll & ~radbsdf.SDsampT
SFLAGS["Ts"] = radbsdf.SDsampAll & ~radbsdf.SDsampR & ~radbsdf.SDsampDf
SFLAGS["Rs"] = radbsdf.SDsampAll & ~radbsdf.SDsampT & ~radbsdf.SDsampDf
SFLAGS["Td"] = radbsdf.SDsampAll & ~radbsdf.SDsampR & ~radbsdf.SDsampSp
SFLAGS["Rd"] = radbsdf.SDsampAll & ~radbsdf.SDsampT & ~radbsdf.SDsampSp


cdef class TabularBSDF:
    """TabularBSDF objects."""

    cdef const radbsdf.SDData* sdata
    cdef object _material
    cdef object _manufacturer
    cdef double _width
    cdef double _height
    cdef double _thickness
    cdef tuple _trns_front_diff
    cdef tuple _trns_back_diff
    cdef tuple _refl_front_diff
    cdef tuple _refl_back_diff
    cdef double _trns_front_hemi_peak
    cdef double _trns_back_hemi_peak
    cdef double _refl_front_hemi_peak
    cdef double _refl_back_hemi_peak

    def __cinit__(self, fpath):
        self.sdata = radbsdf.SDcacheFile(fpath.encode())
        if self.sdata is NULL:
            raise MemoryError()
        self._material = self.sdata.matn.decode()
        self._manufacturer = self.sdata.makr.decode()
        self._width = self.sdata.dim[0]
        self._height = self.sdata.dim[1]
        self._thickness = self.sdata.dim[2]
        self._trns_front_diff = self.sdvalue2xyz(self.sdata.tLambFront)
        self._trns_back_diff = self.sdvalue2xyz(self.sdata.tLambBack)
        self._refl_front_diff = self.sdvalue2xyz(self.sdata.rLambFront)
        self._refl_back_diff = self.sdvalue2xyz(self.sdata.rLambBack)
        if self.sdata.tf:
            self._trns_front_hemi_peak = self.sdata.tLambFront.cieY + self.sdata.tf.maxHemi
        if self.sdata.tb:
            self._trns_back_hemi_peak = self.sdata.tLambFront.cieY + self.sdata.tb.maxHemi
        if self.sdata.rf:
            self._refl_front_hemi_peak = self.sdata.rLambFront.cieY + self.sdata.rf.maxHemi
        if self.sdata.rb:
            self._refl_back_hemi_peak = self.sdata.rLambFront.cieY + self.sdata.rb.maxHemi

    def __dealloc__(self):
        if self.sdata is not NULL:
            radbsdf.SDfreeCache(self.sdata)

    cdef sdvalue2xyz(self, radbsdf.SDValue sval):
        try:
            ciex = sval.spec.cx / sval.spec.cy * sval.cieY
        except ZeroDivisionError:
            ciex = 0
        ciey = sval.cieY
        try:
            ciez = (1 - sval.spec.cx - sval.spec.cy) / sval.spec.cy * sval.cieY
        except ZeroDivisionError:
            ciez = 0
        return (ciex, ciey, ciez)

    @property
    def material(self):
        return self._material

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def width(self):
        return self.sdata.dim[0]

    @property
    def height(self):
        return self._height

    @property
    def thickness(self):
        return self._thickness

    @property
    def trns_front_diff(self):
        return self._trns_front_diff

    @property
    def trns_back_diff(self):
        return self._trns_back_diff

    @property
    def refl_front_diff(self):
        return self._refl_front_diff

    @property
    def refl_back_diff(self):
        return self._refl_back_diff

    @property
    def trns_front_hemi_peak(self):
        return self._trns_front_hemi_peak

    @property
    def trns_back_hemi_peak(self):
        return self._trns_back_hemi_peak

    @property
    def refl_front_hemi_peak(self):
        return self._refl_front_hemi_peak

    @property
    def refl_back_hemi_peak(self):
        return self._refl_back_hemi_peak

    def get_summary(self):
        summary_string = f"Materials: {self.material}\n"
        summary_string += f"Manufacturer: {self.manufacturer}\n"
        summary_string += f"Width, Height, Thickness (m): {self.width} {self.height} {self.thickness}\n"
        summary_string += f"Peak front hemispherical transmittance: {self.trns_front_hemi_peak}\n"
        summary_string += f"Peak back hemispherical transmittance: {self.trns_back_hemi_peak}\n"
        summary_string += f"Peak front hemispherical reflectance: {self.refl_front_hemi_peak}\n"
        summary_string += f"Peak back hemispherical reflectance: {self.refl_back_hemi_peak}\n"
        summary_string += "Diffuse Front Reflectance: {0} {1} {2}\n".format(*self.refl_front_diff)
        summary_string += "Diffuse Back Reflectance: {0} {1} {2}\n".format(*self.refl_back_diff)
        summary_string += "Diffuse Front Transmittance: {0} {1} {2}\n".format(*self.trns_front_diff)
        summary_string += "Diffuse Back Transmittance: {0} {1} {2}\n".format(*self.trns_back_diff)
        print(summary_string)

    cdef get_xyz_from_sdvalue(self, val):
        """Get cie XYZ values from SDValue object."""
        ciex = val.spec.cx / val.spec.cy * val.cieY
        ciey = val.cieY
        ciez = (1 - val.spec.cx - val.spec.cy) / val.spec.cy * val.cieY
        return (ciex, ciey, ciez)


    cpdef query(self, outVec, inVec):
        cdef radbsdf.FVECT outv
        cdef radbsdf.FVECT inv
        cdef radbsdf.SDValue sv

        for i in range(radbsdf.SDmaxCh):
            outv[i] = outVec[i]
            inv[i] = inVec[i]

        err = radbsdf.SDevalBSDF(&sv, outv, inv, self.sdata)
        if err:
            radbsdf.SDError[err]
        else:
            return self.sdvalue2xyz(sv)

    cpdef get_direct_hemi(self, invec, int sflag):
        cdef radbsdf.FVECT inv

        for i in range(radbsdf.SDmaxCh):
            inv[i] = invec[i]

        return radbsdf.SDdirectHemi(inv, sflag, self.sdata)

    cpdef sample(self, int nsamp, ivec, int sflags):
        # cdef radbsdf.FVECT ioVec
        cdef list samples = []
        cdef radbsdf.SDValue val
        cdef double[3] iv = ivec

        for i in range(nsamp):
            randx = (i + rand()*(1./(RAND_MAX+.5)))/nsamp
            err = radbsdf.SDsampBSDF(&val, iv, randx, sflags, self.sdata)
            samples.append(iv + list(self.sdvalue2xyz(val)))

        return samples

    # Query projected solid angle resolution for non-diffuse BSDF direction
    cpdef proj_solid_angle(self, vec1):
        cdef double[2] proja
        cdef radbsdf.FVECT inv

        for i in range(radbsdf.SDmaxCh):
            inv[i] = vec1[i]

        # forcing min max query
        qflags = radbsdf.SDqueryMin + radbsdf.SDqueryMax

        err = radbsdf.SDsizeBSDF(proja, inv, NULL, qflags, self.sdata)
        if err:
            radbsdf.SDError[err]
        else:
            return proja

    # Query projected solid angle resolution for non-diffuse BSDF direction
    cpdef proj_solid_angle2(self, vout, vin):
        cdef double[2] proja
        cdef radbsdf.FVECT inv1
        cdef radbsdf.RREAL[3] inv2

        for i in range(radbsdf.SDmaxCh):
            inv1[i] = vout[i]
            inv2[i] = vin[i]

        # forcing min max query
        qflags = radbsdf.SDqueryMin + radbsdf.SDqueryMax

        err = radbsdf.SDsizeBSDF(proja, inv1, inv2, qflags, self.sdata)
        if err:
            radbsdf.SDError[err]
        else:
            return proja


