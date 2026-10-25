"""Derive CSVs from one rFactor 2 MoTeC .ld log (data-only; no code from the file runs).

Usage: python3 -I derive_rf2.py <file.ld> <out_dir>
Writes: channels_20hz.csv, channel_index.csv, laps_from_lap_number.csv, header_meta.json
The driver field of the header is detected but deliberately never written.
"""
import csv
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ldp", os.path.join(HERE, "ld_parse.py"))
ldp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ldp)

path, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
buf = open(path, "rb").read()
hdr = ldp.read_header(buf)
chans = ldp.read_channels(buf, hdr["meta_ptr"])
by_name = {c["name"]: c for c in chans}


def vals(name):
    return ldp.values(buf, by_name[name])


# channel index (every channel, numeric stats only)
with open(os.path.join(out_dir, "channel_index.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["name", "short_name", "unit", "freq_hz", "n_samples", "duration_s", "dtype", "min", "max", "mean"])
    for c in chans:
        v = ldp.values(buf, c) if c["freq"] else None
        dur = round(c["n"] / c["freq"], 2) if c["freq"] else ""
        if v:
            w.writerow([c["name"], c["short"], c["unit"], c["freq"], c["n"], dur, c["dtype"],
                        round(min(v), 4), round(max(v), 4), round(sum(v) / len(v), 4)])
        else:
            w.writerow([c["name"], c["short"], c["unit"], c["freq"], c["n"], dur, c["dtype"], "", "", ""])

# 20 Hz channels share one time base (n = 11517, 575.85 s); 100 Hz lap number and 5 Hz lap distance are
# looked up by time so every row is one 20 Hz instant.
N20 = by_name["Ground Speed"]["n"]
spd = vals("Ground Speed"); thr = vals("Throttle Pos"); brk = vals("Brake Pos"); clt = vals("Clutch Pos")
str_pct = vals("Steering"); swa = vals("Steering Wheel Position"); tq = vals("Steering Shaft Torque")
rpm = vals("Engine RPM"); gear = vals("Gear")
lap100 = vals("Lap Number"); ld5 = vals("Lap Distance")
with open(os.path.join(out_dir, "channels_20hz.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["t_s", "lap_number", "lap_distance_m", "speed_kmh", "throttle_pct", "brake_pct", "clutch_pct",
                "steering_pct", "steering_wheel_deg", "steering_shaft_torque_nm", "engine_rpm", "gear"])
    for i in range(N20):
        t = i / 20.0
        lap = lap100[min(len(lap100) - 1, int(round(t * 100)))]
        ldist = ld5[min(len(ld5) - 1, int(t * 5))]
        w.writerow([round(t, 3), int(lap), round(ldist, 1), round(spd[i], 2), round(thr[i], 2), round(brk[i], 2),
                    round(clt[i], 2), round(str_pct[i], 2), round(swa[i], 2), round(tq[i], 2),
                    round(rpm[i]), int(gear[i])])

# laps from the 100 Hz lap-number channel (segments of constant value)
lap_seq = lap100
t100 = vals("Session Elapsed Time")
segs, cur, start = [], lap_seq[0], 0
for i in range(1, len(lap_seq)):
    if lap_seq[i] != cur:
        segs.append((int(cur), start, i - 1))
        cur, start = lap_seq[i], i
segs.append((int(cur), start, len(lap_seq) - 1))
last_lt = vals("Last Laptime")
with open(os.path.join(out_dir, "laps_from_lap_number.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["lap_number", "start_session_s", "duration_s", "n_samples_100hz", "complete_for_lap_time",
                "last_laptime_reported_s"])
    for lap_no, a, b in segs:
        dur = round(t100[b] - t100[a], 2)
        reported = round(last_lt[min(b // 20, len(last_lt) - 1)], 2)
        w.writerow([lap_no, round(t100[a], 2), dur, b - a + 1, "yes" if 50 <= dur <= 60 else "no", reported])

meta = {
    "file_bytes": len(buf),
    "date": hdr["date"], "time": hdr["time"], "venue": hdr["venue"],
    "vehicle_id": hdr["vehicle_id"], "event_name": hdr["event_name"], "session": hdr["session"],
    "short_comment": hdr["short_comment"],
    "driver_field": "present (not stored)",
    "channels_in_linked_list": len(chans),
    "channels_header_field": hdr["num_chans_field"],
}
with open(os.path.join(out_dir, "header_meta.json"), "w") as fh:
    json.dump(meta, fh, indent=2, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))
print("20Hz rows:", N20, "| laps:", [(s[0], round(t100[s[2]] - t100[s[1]], 2)) for s in segs])
