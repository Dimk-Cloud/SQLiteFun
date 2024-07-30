'''This module implements a number of user-defined functions via
aggregate classes, as set out in the sqlite3 DB-API 2.0
'''

import statistics
from typing import Callable


# The following Mixin classes apply the DRY principle.
# ----------------------------------------------------
class StatMixin:
    """A Mixin class to be inherited by aggregate classes below
    that produce measures of cenrtral tendency (averages, means, etc)
    and measures of spread (standard deviation and variance).
    """

    def __init__(self):
        self.series = list()
        
    def step(self, elem) -> None: 
        self.series.append(elem)

class WinStatMixin:
    """A Mixin class to be inherited by window functions aggregate classes
    below that produce measures of cenrtral tendency (averages, means, etc)
    and measures of spread (standard deviation and variance).
    """

    def inverse(self, value) -> None:
        self.series.remove(value)

    def value(self, statfun: Callable) -> float | None:
        if len(self.series) == 0:
            return None
        else:
            return statfun(self.series)

    def finalize(self):
        result = type(self).value(self)
        self.series.clear()     # not needed, but you can never be too careful :-)
        return result
        
        
# The following classes are to be used with create_window_function()
# ------------------------------------------------------------------

class WinGeoMean(StatMixin, WinStatMixin):
    """The Geometric Mean of a series, a window function class."""

    def value(self):
        if any(elem == 0 for elem in self.series):
            return 0.0
        return super().value(statistics.geometric_mean)


class WinHarmoMean(StatMixin, WinStatMixin):
    """The Harmonic Mean of a series, a window function class."""

    def value(self):
        if any(elem == 0 for elem in self.series):
            return 0.0
        return super().value(statistics.harmonic_mean)


class WinMode(StatMixin, WinStatMixin):
    """The Mode of a series, a window function class."""

    def value(self):
        return super().value(statistics.mode)

    
class WinMedian(StatMixin, WinStatMixin):
    """The Median of a series, a window function class."""
    
    def value(self):
        return super().value(statistics.median)


class WinStDev(StatMixin, WinStatMixin):
    """The Population Standard Deviation of a series, a window function class."""
    
    def value(self):
        return super().value(statistics.pstdev)

class WinVariance(StatMixin, WinStatMixin):
    """The Population Variance of a series, a window function class."""
    
    def value(self):
        return super().value(statistics.pvariance)
        

# The following classes are to be used with create_aggregate().
# These are legacy classes and no longer needed, as the Window Function classes
# provide the same functionality. Could have tucked away some common functionality
# into StatMixin, but why bother now.
# ----------------------------------------------------------------------------

class GeoMean(StatMixin):
    """The Geometric Mean of a series."""

    def finalize(self) -> float | None:
        if len(self.series) == 0:
            return None
        elif any(elem == 0 for elem in self.series):
            return 0.0
        else:
            #return math.pow(reduce(mul, self.series), 1/len(self.series))
            return statistics.geometric_mean(self.series)


class HarmoMean(StatMixin):
    """The Harmonic Mean of a series."""
    
    def finalize(self) -> float | None:
        if len(self.series) == 0:
            return None
        elif any(elem == 0 for elem in self.series):
            return 0.0
        else:
            # Why does the operator module not include the reciprocal ???????????
            #return len(self.series) / reduce(add, map(lambda x: 1/x, self.series))
            return statistics.harmonic_mean(self.series)


class Mode(StatMixin):
    """The Mode of a series."""
    
    def finalize(self):
        if len(self.series) == 0:
            return None
        else:
            return statistics.mode(self.series)


class Median(StatMixin):
    """The Median of a series."""
    
    def finalize(self):
        if len(self.series) == 0:
            return None
        else:
            return statistics.median(self.series)
    
        
class StDev(StatMixin):
    """The Population Standard Deviation of a series."""
    
    def finalize(self):
        if len(self.series) == 0:
            return None
        else:
            return statistics.pstdev(self.series)
        
        
class Variance(StatMixin):
    """The Population Variance of a series."""
    
    def finalize(self):
        if len(self.series) == 0:
            return None
        else:
            return statistics.pvariance(self.series)









































