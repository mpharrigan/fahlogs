from __future__ import print_function
import re

class Device:
    """Represents an OpenCL Device that FAHClient found."""
    def __init__(self, ma=None):
        if ma is not None:
            self.idx = int(ma.group(1))
            self.name = ma.group(2).strip()
            self.vendor = ma.group(3).strip()
            self.version = ma.group(4).strip()
        else:
            self.idx = -1
            self.name = ""
            self.vendor = ""
            self.version = ""
        
    def __str__(self):
        return "{idx}: {name}; {vendor}; {version}".format(**self.__dict__)
    
    __repr__ = __str__

class Platform:
    """Represents and OpenCL Platform that FAHClient found."""
    def __init__(self, idx, devices):
        self.idx = idx
        self.devices = devices

    def __str__(self):
        return "Platform {} with {} devices".format(self.idx, len(self.devices))

    __repr__ = __str__


class FAHLog:
<<<<<<< HEAD
    dev_res = (r"\s*-- (\d) --\s*\n"
                "\s*DEVICE_NAME = (.+)\n"
                "\s*DEVICE_VENDOR = (.+)\n"
                "\s*DEVICE_VERSION = (.+)\n")
    platform_re = re.compile(r"\(\d+\) device\(s\) found on platform (\d):\n"
                              "({dev_res}\s*)+".format(dev_res=dev_res))
    dev_re = re.compile(dev_res)
    devidx_re = re.compile(r"Arguments passed:.*-gpu (\d)")
    platidx_re = re.compile(r"Looking for vendor: \w+..."
                             "found on platformId (\d+)")
    time_re = re.compile(r"Launch time: ([\d\-T:Z]+)")
    
    def __init__(self, fn, success=True):
        with open(fn) as f:
            s = f.read()
        
        # Parse platforms and their devices
        platform_matches = self.platform_re.finditer(s)
        platforms = dict()
        for platform_ma in platform_matches:
            device_matches = self.dev_re.finditer(platform_ma.group(0))
            devices = [Device(ma) for ma in device_matches]
            devices = dict((d.idx, d) for d in devices)
            plat_idx = int(platform_ma.group(1))
            platforms[plat_idx] = Platform(plat_idx, devices)
        self.platforms = platforms

        # Find which device was actually used
        platidx = int(self.platidx_re.search(s).group(1))
        devidx = int(self.devidx_re.search(s).group(1))
        try:
            self.platform = platforms[platidx]
            self.device = self.platform.devices[devidx]
        except KeyError:
            print("Warning: error parsing", fn)
            self.device = Device()
        
        time_match = self.time_re.search(s).group(1)
        self.time = time_match
        
        # Save some more parameters
        self.success = success
        self.fn = fn
        
    def to_dict(self):
        """Return as a dictionary (for pandas)"""
        return dict(idx=self.device.idx,
                    name=self.device.name,
                    vendor = self.device.vendor,
                    version = self.device.version,
                    success = self.success,
                    time = self.time,
                    fn = self.fn)
    
    def __str__(self):
        return str(self.to_dict())
    
    __repr__ = __str__

