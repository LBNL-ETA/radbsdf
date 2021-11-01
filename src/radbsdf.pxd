# Extending from the Radiance src/common/bsdf.h header file
from libc.stdio cimport FILE
from libc.stdlib cimport rand

cdef extern from "limits.h":
    int RAND_MAX

cdef extern int rand()
cdef extern printf()

cdef extern from '../Radiance/src/common/bsdf.h':

    # maximum # spectral channels
    const int SDmaxCh

    # maximum BSDF name length
    const int SDnameLn

    # Component flags for SDsampBSDF() and SDdirectHemi()
    const int SDsampR # include reflection
    const int SDsampT # include transmission
    const int SDsampS # include scattering (R+T)
    const int SDsampSp # include non-diffuse portion
    const int SDsampDf # include diffuse portion
    const int SDsampSpR # include non-diffuse reflection
    const int SDsampSpT	 # include non-diffuse transmission
    const int SDsampSpS	 # include non-diffuse scattering
    const int SDsampAll	 # include everything

    # Projected solid angle query flags for SDsizeBSDF()
    const int SDqueryVal
    const int SDqueryMin
    const int SDqueryMax


    ctypedef double FVECT[SDmaxCh]

    ctypedef float RREAL

    #
    ctypedef struct C_COLOR:
        int clock
        void *client_data
        short flags
        short ssamp[41]
        long ssum
        float cx
        float cy
        float eff


    # Holder for BSDF value and spectral color
    ctypedef struct SDValue:
        double cieY
        C_COLOR spec

    # Cached, encoded, cumulative distribution
    # for one incident (solid) angle
    cdef SD_CDIST_BASE(styp)

    cdef double cTotal

    cdef struct SDCDst_s:
        SD_CDIST_BASE(SDCDst_s)

    ctypedef SDCDst_s SDCDst
    cdef SDCDst SDemptyCD # empty distribution

    # Structure to hold a spectral BSDF component (typedef SDComponent above) */
    cdef struct SDComp_s:
        C_COLOR cspec[SDmaxCh]
        const SDFunc *func
        void *dist
        SDCDst *cdList

    # Forward declaration of BSDF component
    ctypedef SDComp_s SDComponent

    # Methods needed to handle BSDF components (nothing is optional) */
    ctypedef struct SDFunc:

        # return non-diffuse BSDF
        int (*getBSDFs)(float coef[SDmaxCh], const FVECT outVec,
                        const FVECT inVec, SDComponent *sdc)

        # query non-diffuse PSA for vector
        SDError (*queryProjSA)(double *psa, const FVECT v1,
                               const RREAL *v2, int qflags, SDComponent *sdc)

        # get cumulative distribution
        const SDCDst *(*getCDist)(const FVECT inVec, SDComponent *sdc)

        # sample cumulative distribution
        SDError     (*sampCDist)(FVECT ioVec, double randX, const SDCDst *cdp)

        # free a spectral BSDF component
        void     (*freeSC)(void *dist)



    # Container for non-diffuse BSDF components
    ctypedef struct SDSpectralDF:
        double minProjSA
        double maxHemi
        int ncomp
        SDComponent comp[1]

    # Loaded BSDF data
    ctypedef struct SDData:
        char name[SDnameLn]
        char matn[SDnameLn]
        char makr[SDnameLn]
        char *mgf
        double dim[SDmaxCh]
        SDValue rLambFront
        SDValue rLambBack
        SDValue tLambFront
        SDValue tLambBack
        SDSpectralDF *rf
        SDSpectralDF *rb
        SDSpectralDF *tf
        SDSpectralDF *tb

    # Error codes: normal return, out of memory, file i/o, file format,
    # bad argument, bad data, unsupported feature,
    # internal error, unknown error
    ctypedef enum SDError:
        SDEnone=0,
        SDEmemory,
        SDEfile,
        SDEformat,
        SDEargument,
        SDEdata,
        SDEsupport,
        SDEinternal,
        SDEunknown

    # Get BSDF from cache (or load and cache it on first call)
    # Report any problems to stderr, return NULL on failure
    const SDData* SDcacheFile(const char* fname)

    # Free a BSDF from our cache (clear all if sd==NULL) */
    #void SDfreeCache(const SDData* sd)
    void SDfreeCache

    # Query projected solid angle resolution for non-diffuse BSDF direction(s) */
    SDError SDsizeBSDF(double* projSA, const FVECT v1,
                       const RREAL* v2, int qflags,
                       const SDData* sd)

    # Return BSDF for the given incident and scattered ray vectors */
    SDError SDevalBSDF(SDValue* sv, const FVECT outVec,
                       const FVECT inVec, const SDData* sd)

    # Compute directional hemispherical scattering at given incident angle */
    double SDdirectHemi(const FVECT inVec, int sflags, const SDData* sd)

    # Sample BSDF direction based on the given random variable */
    SDError SDsampBSDF(SDValue* sv, FVECT ioVec, double randX, int sflags, const SDData* sd)

    # List of loaded BSDFs */
    # ctypedef struct SDCache_s:
        # SDData bsdf # BSDF data */
        # unsigned refcnt		# how many callers are using us? */
        # SDCache_s		# next in cache list */
            # *next
    # } *SDcacheList		# Global BSDF cache */

    extern int		SDretainSet	# =SDretainNone by default */
    extern unsigned long	SDmaxCache	# =0 (unlimited) by default */

    ##################################################################
    # The following routines are less commonly used by applications.
    ##################################################################

    int SDisLoaded(sd)

    # Report an error to the indicated stream */
    SDError SDreportError(SDError ec, FILE *fp)

    # Shorten file path to useable BSDF name, removing suffix */
    void SDclipName(char res[SDnameLn], const char *fname)

    # Allocate new spectral distribution function */
    SDSpectralDF *SDnewSpectralDF(int nc)

    # Add component(s) to spectral distribution function */
    SDSpectralDF *SDaddComponent(SDSpectralDF *odf, int nadd)

    # Free a spectral distribution function */
    void SDfreeSpectralDF(SDSpectralDF *df)

    # Initialize an unused BSDF struct and assign name (calls SDclipName) */
    void SDclearBSDF(SDData *sd, const char *fname)

    # Load a BSDF struct from the given file (keeps name unchanged) */
    SDError SDloadFile(SDData *sd, const char *fname)

    # Free data associated with BSDF struct */
    void SDfreeBSDF(SDData *sd)

    # Find writeable BSDF by name, or allocate new cache entry if absent */
    SDData *SDgetCache(const char *bname)

    # Free cached cumulative distributions for BSDF component */
    void SDfreeCumulativeCache(SDSpectralDF *df)

    # Sample an individual BSDF component */
    SDError SDsampComponent(SDValue *sv, FVECT ioVec, double randX, SDComponent *sdc)

    # Convert 1-dimensional random variable to N-dimensional */
    void SDmultiSamp(double t[], int n, double randX)

    # Map a [0,1]^2 square to a unit radius disk */
    void SDsquare2disk(double ds[2], double seedx, double seedy)

    # Map point on unit disk to a unit square in [0,1]^2 range */
    void SDdisk2square(double sq[2], double diskx, double disky)


    ##################################################################
    # Vector math for getting between world and local BSDF coordinates.
    # Directions may be passed unnormalized to these routines.
    ##################################################################

    # Compute World->BSDF transform from surface normal and BSDF up vector */
    SDError SDcompXform(RREAL vMtx[3][3], const FVECT sNrm, const FVECT uVec)

    # Compute inverse transform */
    SDError SDinvXform(RREAL iMtx[3][3], RREAL vMtx[3][3])

    # Transform and normalize direction (column) vector */
    SDError SDmapDir(FVECT resVec, RREAL vMtx[3][3], const FVECT inpVec)

    # Application-specific BSDF loading routine (not part of our library) */
    SDData *loadBSDF(char *name)

    # Application-specific BSDF error translator (not part of our library) */
    char *transSDError(SDError ec)
