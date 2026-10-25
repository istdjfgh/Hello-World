"""Minimal MoTeC .ld reader (own implementation, layout taken from public
reader sources as reference only). Data-only: never executes file content.

Usage: python3 -I ld_parse.py <file.ld> [channel_name ...]
Prints header fields, channel table and, if asked, per-channel stats.
"""
import struct
import sys


def cstr(b):
    return b.split(b"\x00", 1)[0].decode("latin-1", "replace").strip()


def read_header(buf):
    if struct.unpack_from("<I", buf, 0)[0] != 0x40:
        raise ValueError("not an LD file (marker != 0x40)")
    meta_ptr, data_ptr = struct.unpack_from("<II", buf, 8)
    event_ptr = struct.unpack_from("<I", buf, 36)[0]
    num_chans = struct.unpack_from("<I", buf, 86)[0]
    date = cstr(buf[94:110])
    time_ = cstr(buf[126:142])
    driver = cstr(buf[158:222])
    vehicle_id = cstr(buf[222:286])
    venue = cstr(buf[350:414])
    short_comment = cstr(buf[1572:1636])
    event_name = session = None
    if event_ptr:
        event_name = cstr(buf[event_ptr:event_ptr + 64])
        session = cstr(buf[event_ptr + 64:event_ptr + 128])
    return {
        "meta_ptr": meta_ptr, "data_ptr": data_ptr, "num_chans_field": num_chans,
        "date": date, "time": time_, "driver_field": driver, "vehicle_id": vehicle_id,
        "venue": venue, "short_comment": short_comment,
        "event_name": event_name, "session": session,
    }


DTYPE_FMT = {("int8", 1): "<b", ("int16", 2): "<h", ("int32", 4): "<i", ("float32", 4): "<f", ("float16", 2): "<e"}


def read_channels(buf, meta_ptr):
    chans = []
    ptr = meta_ptr
    seen = set()
    while ptr and ptr not in seen and ptr + 124 <= len(buf):
        seen.add(ptr)
        prev_ptr, next_ptr, data_ptr, data_len = struct.unpack_from("<IIII", buf, ptr)
        dtype_a, dtype_raw, freq, shift, mul, scale, dec = struct.unpack_from("<HHHhhhh", buf, ptr + 18)
        name = cstr(buf[ptr + 32:ptr + 64])
        short = cstr(buf[ptr + 64:ptr + 72])
        unit = cstr(buf[ptr + 72:ptr + 84])
        if dtype_a == 0x07:
            dtype = {2: "float16", 4: "float32"}.get(dtype_raw)
        elif dtype_a in (0, 0x03, 0x05):
            dtype = {1: "int8", 2: "int16", 4: "int32"}.get(dtype_raw)
        else:
            dtype = None
        chans.append({
            "name": name, "short": short, "unit": unit, "freq": freq, "n": data_len,
            "data_ptr": data_ptr, "dtype": dtype, "dtype_raw": dtype_raw,
            "shift": shift, "mul": mul, "scale": scale, "dec": dec,
        })
        ptr = next_ptr
    return chans


def values(buf, ch):
    """Physical value. Order verified on this file: raw*mul/scale*10^-dec + shift
    (gives ~141 km/h, ~7300 rpm, 0..100 % pedals). Applying shift before mul is wrong."""
    if ch["dtype"] is None or ch["scale"] == 0 or (ch["dtype"], ch["dtype_raw"]) not in DTYPE_FMT:
        return None
    fmt = DTYPE_FMT[(ch["dtype"], ch["dtype_raw"])]
    size = struct.calcsize(fmt)
    out = []
    p = ch["data_ptr"]
    for i in range(ch["n"]):
        raw = struct.unpack_from(fmt, buf, p + i * size)[0]
        out.append(raw * ch["mul"] / ch["scale"] * 10 ** (-ch["dec"]) + ch["shift"])
    return out


def main():
    path = sys.argv[1]
    want = sys.argv[2:]
    buf = open(path, "rb").read()
    hdr = read_header(buf)
    print("FILE", path, "bytes", len(buf))
    for k, v in hdr.items():
        if k == "driver_field":
            print(f"  driver_field: present={bool(v)} (value not printed)")
        else:
            print(f"  {k}: {v}")
    chans = read_channels(buf, hdr["meta_ptr"])
    print(f"  channels parsed: {len(chans)} (header says {hdr['num_chans_field']})")
    print("  name | short | unit | freq_hz | n | duration_s | dtype | scale dec mul shift")
    for c in chans:
        dur = c["n"] / c["freq"] if c["freq"] else None
        print(f"  {c['name']} | {c['short']} | {c['unit']} | {c['freq']} | {c['n']} | "
              f"{dur:.2f} | {c['dtype']} | {c['scale']} {c['dec']} {c['mul']} {c['shift']}"
              if dur is not None else f"  {c['name']} | {c['short']} | {c['unit']} | {c['freq']} | {c['n']} | - | {c['dtype']}")
    for c in chans:
        if want and c["name"] not in want:
            continue
        vals = values(buf, c)
        if not vals:
            print("  no data:", c["name"])
            continue
        mn, mx = min(vals), max(vals)
        mean = sum(vals) / len(vals)
        print(f"  STAT {c['name']} [{c['unit']}] min={mn:.4f} max={mx:.4f} mean={mean:.4f} n={len(vals)}")


if __name__ == "__main__":
    main()
