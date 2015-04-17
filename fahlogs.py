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



class FAHLog:

    dev_re = re.compile(r"\s*-- (\d) --\s*\n"
                         "\s*DEVICE_NAME = (.+)\n"
                         "\s*DEVICE_VENDOR = (.+)\n"
                         "\s*DEVICE_VERSION = (.+)\n")
    arg_re = re.compile(r"Arguments passed:.*-gpu (\d)")
    time_re = re.compile(r"Launch time: ([\d-T:Z]+)"
    
    def __init__(self, fn, success=True):
        with open(fn) as f:
            s = f.read()
            device_matches = self.dev_re.finditer(s)
            arg_match = int(self.arg_re.search(s).group(1))
            time_match = self.time_re.search(s).group(1)
            
        devices = [Device(ma) for ma in device_matches]
        devices = dict((d.idx, d) for d in devices)
        
        self.devices = devices
        try:
            self.device = self.devices[arg_match]
        except KeyError:
            print("Warning: error parsing", fn)
            self.device = Device()
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

