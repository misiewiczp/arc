"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class distance_t(object):
    __slots__ = ["timestamp", "measure"]

    __typenames__ = ["int64_t", "int16_t"]

    __dimensions__ = [None, None]

    def __init__(self):
        self.timestamp = 0
        self.measure = 0

    def encode(self):
        buf = BytesIO()
        buf.write(distance_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qh", self.timestamp, self.measure))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != distance_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return distance_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = distance_t()
        self.timestamp, self.measure = struct.unpack(">qh", buf.read(10))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if distance_t in parents: return 0
        tmphash = (0x3bb5fab93238edf3) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if distance_t._packed_fingerprint is None:
            distance_t._packed_fingerprint = struct.pack(">Q", distance_t._get_hash_recursive([]))
        return distance_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
