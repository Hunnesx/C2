import numpy as np
from scipy.integrate import quad
from scipy.optimize import newton

R = 83.15
# Values for which you are interested to find the maxwell pressure
T = 288.7
a = 3.658*10**6
b = 42.75
R


def vdw(V):
    """Van der Waals equation of state.

    Return the pressure for a given volume.

    """

    p = n*R*T/(V-n*b)-n**2*a/V**2
    return p


def vdw_maxwell(Vi):
    """
    Return a value for the maxwell pressure.

    Vi is an estimate for the mean of the Volumes at which the p(V)-curve takes its local maximum/minimum.
    """

    def get_vlims(p):
        """
        Return the smallest and largest volume for which the gas pressure is p.
        """

        eos = np.poly1d([p, -(n*b*p+n*R*T), n**2*a, -n**3*b*a])
        roots = eos.r
        roots.sort()
        vmin, vmid, vmax = roots
        return vmin, vmax

    def get_area_difference(v0):
        """
        Return the difference in areas of the van der Waals loops.

        Return the difference in areas between the p(v)-graph and the p(v0)-line between the vmin-v0 section
        and the v0-vmax section. If this difference is 0, then p(v0) = p_maxwell

        """

        p0 = vdw(v0)
        vmin, vmax = get_vlims(p0)
        return quad(lambda v: vdw(v) - p0, vmin, vmax)[0]

    # Root finding by Newton's method determines Vr0 corresponding to
    # equal loop areas for the Maxwell construction.
    vfinal = newton(get_area_difference, Vi)
    pr0 = vdw(vfinal)
    return pr0


print(vdw_maxwell(140))
