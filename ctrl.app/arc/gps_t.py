"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class gps_t(object):
    __slots__ = ["timestamp", "fix_time", "fix_date", "lat", "lon", "vel"]

    __typenames__ = ["int64_t", "int32_t", "int32_t", "float", "float", "float"]

    __dimensions__ = [None, None, None, None, None, None]

    def __init__(self):
        self.timestamp = 0
        self.fix_time = 0
        self.fix_date = 0
        self.lat = 0.0
        self.lon = 0.0
        self.vel = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(gps_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qiifff", self.timestamp, self.fix_time, self.fix_date, self.lat, self.lon, self.vel))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != gps_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return gps_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = gps_t()
        self.timestamp, self.fix_time, self.fix_date, self.lat, self.lon, self.vel = struct.unpack(">qiifff", buf.read(28))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if gps_t in parents: return 0
        tmphash = (0xd116511827aa34db) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if gps_t._packed_fingerprint is None:
            gps_t._packed_fingerprint = struct.pack(">Q", gps_t._get_hash_recursive([]))
        return gps_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

