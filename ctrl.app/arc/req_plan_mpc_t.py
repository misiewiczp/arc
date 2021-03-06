"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class req_plan_mpc_t(object):
    __slots__ = ["timestamp", "x", "y", "yaw", "vel", "acc", "dir", "ref_vel", "latency", "npoints", "points_x", "points_y"]

    __typenames__ = ["int64_t", "double", "double", "double", "double", "double", "double", "double", "double", "int32_t", "double", "double"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, ["npoints"], ["npoints"]]

    def __init__(self):
        self.timestamp = 0
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.vel = 0.0
        self.acc = 0.0
        self.dir = 0.0
        self.ref_vel = 0.0
        self.latency = 0.0
        self.npoints = 0
        self.points_x = []
        self.points_y = []

    def encode(self):
        buf = BytesIO()
        buf.write(req_plan_mpc_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qddddddddi", self.timestamp, self.x, self.y, self.yaw, self.vel, self.acc, self.dir, self.ref_vel, self.latency, self.npoints))
        buf.write(struct.pack('>%dd' % self.npoints, *self.points_x[:self.npoints]))
        buf.write(struct.pack('>%dd' % self.npoints, *self.points_y[:self.npoints]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != req_plan_mpc_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return req_plan_mpc_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = req_plan_mpc_t()
        self.timestamp, self.x, self.y, self.yaw, self.vel, self.acc, self.dir, self.ref_vel, self.latency, self.npoints = struct.unpack(">qddddddddi", buf.read(76))
        self.points_x = struct.unpack('>%dd' % self.npoints, buf.read(self.npoints * 8))
        self.points_y = struct.unpack('>%dd' % self.npoints, buf.read(self.npoints * 8))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if req_plan_mpc_t in parents: return 0
        tmphash = (0xfd3b38eeb5705ac6) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if req_plan_mpc_t._packed_fingerprint is None:
            req_plan_mpc_t._packed_fingerprint = struct.pack(">Q", req_plan_mpc_t._get_hash_recursive([]))
        return req_plan_mpc_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

