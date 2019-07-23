"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class res_plan_mpc_t(object):
    __slots__ = ["timestamp", "req_timestamp", "delta_dir", "delta_acc", "npoints", "points_x", "points_y"]

    __typenames__ = ["int64_t", "int64_t", "double", "double", "int32_t", "double", "double"]

    __dimensions__ = [None, None, None, None, None, ["npoints"], ["npoints"]]

    def __init__(self):
        self.timestamp = 0
        self.req_timestamp = 0
        self.delta_dir = 0.0
        self.delta_acc = 0.0
        self.npoints = 0
        self.points_x = []
        self.points_y = []

    def encode(self):
        buf = BytesIO()
        buf.write(res_plan_mpc_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qqddi", self.timestamp, self.req_timestamp, self.delta_dir, self.delta_acc, self.npoints))
        buf.write(struct.pack('>%dd' % self.npoints, *self.points_x[:self.npoints]))
        buf.write(struct.pack('>%dd' % self.npoints, *self.points_y[:self.npoints]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != res_plan_mpc_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return res_plan_mpc_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = res_plan_mpc_t()
        self.timestamp, self.req_timestamp, self.delta_dir, self.delta_acc, self.npoints = struct.unpack(">qqddi", buf.read(36))
        self.points_x = struct.unpack('>%dd' % self.npoints, buf.read(self.npoints * 8))
        self.points_y = struct.unpack('>%dd' % self.npoints, buf.read(self.npoints * 8))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if res_plan_mpc_t in parents: return 0
        tmphash = (0x19739f11f8ec7910) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if res_plan_mpc_t._packed_fingerprint is None:
            res_plan_mpc_t._packed_fingerprint = struct.pack(">Q", res_plan_mpc_t._get_hash_recursive([]))
        return res_plan_mpc_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
