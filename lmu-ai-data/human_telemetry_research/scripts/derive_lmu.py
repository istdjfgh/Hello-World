"""Derive per-lap summary and per-sample CSVs from LMU Desktop's SQLite lap DB.

Usage: python3 -I derive_lmu.py <prisma/dev.db> <out_dir>
Reads only Lap / Session / Track / ImportedLap telemetry columns, read-only.
Never reads ownerName or User.name: no personal data leaves this script.
"""
import csv
import json
import os
import sqlite3
import statistics
import sys

db, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
con = sqlite3.connect("file:" + os.path.abspath(db) + "?mode=ro&immutable=1", uri=True)
con.row_factory = sqlite3.Row

TRACK_MAP = {
    "Circuit de Spa-Francorchamps": ("Spa-Francorchamps", ""),
    "Sebring International Raceway": ("Sebring", "International"),
    "Autodromo Enzo e Dino Ferrari": ("Imola", ""),
    "Paul Ricard - 1A-V2": ("Paul Ricard", "1A-V2"),
}

OWN_SQL = """
select l.id as lap_id, l.lapNumber, l.lapTime, l.isValid, l.sector1, l.sector2, l.sector3,
       l.telemetryJson, s.car, s.carClass, s.type as session_type, t.name as track
from Lap l left join Session s on s.id = l.sessionId left join Track t on t.id = s.trackId
where l.telemetryJson is not null order by s.startedAt, l.lapNumber
"""
IMP_SQL = """
select id as lap_id, lapNumber, lapTime, isValid, sector1, sector2, sector3,
       telemetryJson, car, carClass, type as session_type, trackName as track
from ImportedLap where telemetryJson is not null order by originalCreatedAt
"""

SUMMARY_FIELDS = [
    "lap_key", "origin", "track", "layout", "car_make", "car_class_as_recorded", "session_type",
    "lap_number", "lap_time_s", "is_valid", "sector1_s", "sector2_s", "sector3_s",
    "duration_s", "n_samples", "samples_per_s", "dup_t_fraction", "lap_dist_max_m",
    "speed_max_kmh", "rpm_min", "rpm_max", "gears_seen", "steer_abs_p95", "steer_distinct",
    "steer_frac_at_limit", "throttle_frac_full", "brake_frac_nonzero", "usable", "notes",
]
SAMPLE_FIELDS = ["lap_key", "t_s", "new_t", "lap_dist_m", "speed_kmh", "throttle_norm",
                 "brake_norm", "steer_norm", "rpm", "gear", "x_m", "z_m", "abs_flag", "tc_flag"]


def pctl(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p * (len(xs) - 1))))]


def summarize(origin, idx, r):
    samples = json.loads(r["telemetryJson"])
    n = len(samples)
    lap_key = f"{'OWN' if origin == 'own' else 'IMP'}-{idx:03d}"
    t = [s["t"] for s in samples]
    dup = sum(1 for a, b in zip(t, t[1:]) if a == b) / max(1, n - 1)
    dur = t[-1] - t[0]
    st = [s["st"] for s in samples]
    th = [s["th"] for s in samples]
    br = [s["br"] for s in samples]
    v = [s.get("v", 0) for s in samples]
    rpm = [s["rpm"] for s in samples]
    d = [s["d"] for s in samples]
    track, layout = TRACK_MAP.get(r["track"], (r["track"], ""))
    lap_time = float(r["lapTime"])
    is_valid = bool(r["isValid"])
    sps = n / dur if dur > 0 else 0.0
    if lap_time <= 0 or not is_valid:
        usable, note = "no", "lap_time=0 or invalid lap (incomplete)"
    elif sps > 25:
        usable, note = "yes_after_dedupe", f"{sps:.0f} rows/s: repeated timestamps, dedupe by new_t"
    else:
        usable, note = "yes", ""
    if r["session_type"] == "race" and r["lapNumber"] == 1:
        note = (note + "; " if note else "") + "race lap 1 (standing start)"
    return {
        "lap_key": lap_key, "origin": "own_lap_table" if origin == "own" else "imported_lap_table",
        "track": track, "layout": layout, "car_make": r["car"], "car_class_as_recorded": r["carClass"],
        "session_type": r["session_type"], "lap_number": r["lapNumber"], "lap_time_s": round(lap_time, 3),
        "is_valid": is_valid, "sector1_s": r["sector1"], "sector2_s": r["sector2"], "sector3_s": r["sector3"],
        "duration_s": round(dur, 3), "n_samples": n, "samples_per_s": round(sps, 2),
        "dup_t_fraction": round(dup, 3), "lap_dist_max_m": round(max(d), 1),
        "speed_max_kmh": round(max(v), 1), "rpm_min": min(rpm), "rpm_max": max(rpm),
        "gears_seen": "/".join(str(g) for g in sorted({s["g"] for s in samples})),
        "steer_abs_p95": round(pctl([abs(x) for x in st], 0.95), 4),
        "steer_distinct": len({round(x, 3) for x in st}),
        "steer_frac_at_limit": round(sum(abs(x) >= 0.99 for x in st) / n, 4),
        "throttle_frac_full": round(sum(x >= 0.99 for x in th) / n, 4),
        "brake_frac_nonzero": round(sum(x > 0 for x in br) / n, 4),
        "usable": usable, "notes": note,
    }, samples, lap_key


summaries, all_rows = [], []
idx_own = idx_imp = 0
for r in con.execute(OWN_SQL):
    idx_own += 1
    s, samples, key = summarize("own", idx_own, r)
    summaries.append(s); all_rows.append((key, samples))
for r in con.execute(IMP_SQL):
    idx_imp += 1
    s, samples, key = summarize("imp", idx_imp, r)
    summaries.append(s); all_rows.append((key, samples))

with open(os.path.join(out_dir, "laps_summary.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=SUMMARY_FIELDS)
    w.writeheader(); w.writerows(summaries)

n_samples_total = 0
with open(os.path.join(out_dir, "samples.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=SAMPLE_FIELDS)
    w.writeheader()
    for key, samples in all_rows:
        prev_t = None
        for s in samples:
            w.writerow({
                "lap_key": key, "t_s": s["t"], "new_t": int(s["t"] != prev_t),
                "lap_dist_m": s["d"], "speed_kmh": s.get("v"), "throttle_norm": s["th"],
                "brake_norm": s["br"], "steer_norm": s["st"], "rpm": s["rpm"], "gear": s["g"],
                "x_m": s.get("x"), "z_m": s.get("z"), "abs_flag": s.get("abs"), "tc_flag": s.get("tc"),
            })
            prev_t = s["t"]
            n_samples_total += 1

tally = {}
for s in summaries:
    if s["usable"].startswith("yes"):
        tally[(s["track"], s["layout"], s["car_class_as_recorded"])] = tally.get((s["track"], s["layout"], s["car_class_as_recorded"]), 0) + 1
print("laps_with_telemetry:", len(summaries), "| usable (yes*):", sum(1 for s in summaries if s["usable"].startswith("yes")))
print("samples written:", n_samples_total)
for k, v in sorted(tally.items()):
    print("usable by (track, layout, class):", k, v)
con.close()
