import os
import pyfits
import healpy
import numpy
import astropy.units as units
from astropy.coordinates import SkyCoord

from ToolBox.Astro import Fetchers
from astroquery.irsa_dust import IrsaDust
from sncosmo import dustmap

def test():
    print "test"

def load_map(map=0):
    """
    map is either 
    0: sfd
    1: schlafly
    2: std_s
    3: sfd_n
    """
    if map == 0:
        map = os.getenv('HOME') + '/.extinction/maps/lambda_sfd_ebv.fits'
        hmap = healpy.read_map(map)
    elif map == 1:
        map = os.getenv('HOME') + '/.extinction/maps/ps1-ebv-4.5kpc.fits'
        map = pyfits.getdata(map)
        hmap = map['ebv']
    elif map == 2:
        map = os.getenv('HOME') + '/.extinction/maps/SFD_dust_4096_sgp.fits'
        hmap = pyfits.getdata(map)
    elif map == 3:
        map = os.getenv('HOME') + '/.extinction/maps/SFD_dust_4096_ngp.fits'
        hmap = pyfits.getdata(map)
    return hmap

def plot_map(map=0):
    """
    map is either 
    0: sfd
    1: schlafly
    2: std_s
    3: sfd_n
    """
    if map == 0:
        title = 'SFD E(B-V) map'
    elif map == 1:
        title = 'Schlafly E(B-V) map'

    map = load_map(map)
    healpy.mollview(map, title=title, unit='mag',
                    norm='hist', min=0, max=0.5, xsize=2000)
    healpy.graticule()
    #healpy.gnomview(map, rot=[0,0.3], title='GnomView', unit='mK', format='%.2g')

def get_value(ra, dec, map=0):
    """
    Make some tests
    """
    # Parse input
    coordinates = SkyCoord(ra=ra, dec=dec,
                           unit=units.degree) 

    # Convert to galactic coordinates.
    l = coordinates.galactic.l.degree
    b = coordinates.galactic.b.degree
    print "l, b = %.3f, %.3f" % (l, b)
    m = load_map(map)
    ebv = healpy.get_interp_val(m,  (90.-b)*numpy.pi/180., l*numpy.pi/180.)
    t = IrsaDust.get_extinction_table('%.4f %.4f' % (ra, dec))
    if map in [0, 2, 3]:
        t = t[9]['A_SFD'] / t[9]['A_over_E_B_V_SFD']
    else:
        t = t[9]['A_SandF'] / t[9]['A_over_E_B_V_SandF']
        print t
    f = Fetchers.sfd_ebmv(ra, dec)
    sn = dustmap.get_ebv_from_map([ra, dec], mapdir='/home/chotard/.extinction/maps/')
    print ebv, t, f, sn
