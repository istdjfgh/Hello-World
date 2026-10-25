"""Build catalog.csv from the derived outputs and the verified source list.

Usage: python3 -I build_catalog.py <prisma/dev.db> <derived_root> <catalog.csv>
Only session dates are read from the lap DB; no personal fields are touched.
"""
import csv
import json
import os
import sqlite3
import sys

db, derived, out = sys.argv[1], sys.argv[2], sys.argv[3]
HEAD_SHA = "54a6df1508b5b490f93bd72eb22684227d1d7431"
DEVDB_SHA256 = "a5b94f1d4c772a101dfec28090e3118fa456a322a0cbb58fb15a7a4344cb55a6"
LD_SHA256 = "9e2216ec16d13cbe3ad85eb3004d0c12a8093a039f9e80702750e8718e7c79b4"
LDX_SHA256 = "69dffc48d1ce7acfa4e04a6d7045fca7f14ebe241329c8827056bc75451a663c"
RF2_SHA = "614bac78b70a76f01cbbbaae5a7feb3e51cb0f07"
LD_NAME = "2025-08-03 - 16-34-45 - Matsusaka East Circuit - P1.ld"
LMU_DEVDB = "https://github.com/LMU-Tracking-Desktop/tracker/blob/" + HEAD_SHA + "/prisma/dev.db"
RF2_FILE = ("https://github.com/orion-miller/RFactor2-Motec-Workspace/blob/" + RF2_SHA
            + "/Sample%20Dataset%20-%20Matsusaka%20(Suzuka)/" + LD_NAME.replace(" ", "%20"))

COLUMNS = ["track", "layout", "car", "class", "game", "source_url", "file_url", "format", "channels", "hz",
           "laps", "best_lap", "input_device", "wheel_rotation_deg", "game_version", "date", "author",
           "license", "access", "downloaded", "sha256", "verified", "notes"]

# session start dates in the same order the derive script uses for lap_key numbering
con = sqlite3.connect("file:" + os.path.abspath(db) + "?mode=ro&immutable=1", uri=True)
own_dates = [r[0][:10] for r in con.execute(
    "select s.startedAt from Lap l left join Session s on s.id = l.sessionId "
    "where l.telemetryJson is not null order by s.startedAt, l.lapNumber")]
imp_dates = [r[0][:10] for r in con.execute(
    "select originalCreatedAt from ImportedLap where telemetryJson is not null order by originalCreatedAt")]
con.close()
date_of = {f"OWN-{i + 1:03d}": d for i, d in enumerate(own_dates)}
date_of.update({f"IMP-{i + 1:03d}": d for i, d in enumerate(imp_dates)})

rows = []
for r in csv.DictReader(open(os.path.join(derived, "lmu_desktop_devdb", "laps_summary.csv"))):
    key = r["lap_key"]
    usable = r["usable"]
    st_note = ""
    if key == "OWN-010":
        st_note = "5% of samples at full steering lock: wheel with small range or gamepad? check. "
    if key == "OWN-011":
        st_note = "sample rows duplicated (78 rows/s); dedupe by new_t before use. "
    if usable == "no":
        input_dev = "unknown"
    elif usable == "yes_after_dedupe":
        input_dev = "wheel (likely; not confirmed)"
    elif key == "OWN-010":
        input_dev = "wheel? (unconfirmed; see notes)"
    else:
        input_dev = "wheel (likely; not confirmed)"
    rows.append({
        "track": r["track"],
        "layout": r["layout"] or "base/not stated",
        "car": f"{r['car_make']} (make only; model not recorded)",
        "class": f"{r['car_class_as_recorded']} (as recorded by app)",
        "game": "LMU",
        "source_url": "https://github.com/LMU-Tracking-Desktop/tracker",
        "file_url": LMU_DEVDB,
        "format": "SQLite Lap.telemetryJson (JSON array of samples, one lap); derived CSV",
        "channels": "t_s, lap_dist_m, speed_kmh, throttle_norm, brake_norm, steer_norm(-1..1), rpm, gear, "
                    "x_m, z_m, abs_flag, tc_flag; no clutch; no steering in degrees",
        "hz": "inputs ~15 samples/s; t and lap distance update ~5 Hz",
        "laps": 1,
        "best_lap": f"{r['lap_time_s']} s (this lap's time, not session best)",
        "input_device": input_dev,
        "wheel_rotation_deg": "not recorded (steer normalised -1..1; wheel range unknown)",
        "game_version": "not recorded; session dates 2026-04-19..2026-05-08 (LMU v1.3 released 31 Mar 2026; exact build unknown)",
        "date": date_of.get(key, ""),
        "author": "not stated (nickname only in source)",
        "license": "MIT (README; no LICENSE file in repo)",
        "access": "free",
        "downloaded": "no: raw DB not kept (personal data in file); derived in derived/lmu_desktop_devdb/",
        "sha256": DEVDB_SHA256 + " (prisma/dev.db, HEAD)",
        "verified": "yes",
        "notes": (f"usable={usable}; {r['notes']}; {st_note}samples/s={r['samples_per_s']}; "
                  f"dup_t_fraction={r['dup_t_fraction']}; origin={r['origin']}; "
                  f"speed_max={r['speed_max_kmh']} km/h; steer_p95_abs={r['steer_abs_p95']}")
                 .replace("; ;", ";").strip("; "),
    })

meta = json.load(open(os.path.join(derived, "rf2_matsusaka_p1", "header_meta.json")))
rows.append({
    "track": "Matsusaka East Circuit (rFactor 2 track; NOT an LMU track)",
    "layout": "not stated",
    "car": "not recorded (vehicle_id empty)",
    "class": "not recorded",
    "game": "rF2 (fallback layer, not LMU)",
    "source_url": "https://github.com/orion-miller/RFactor2-Motec-Workspace",
    "file_url": RF2_FILE,
    "format": "MoTeC .ld (+ .ldx, XML with setup values, no lap markers)",
    "channels": "245 in linked list (header field says 78): Ground Speed, Throttle/Brake/Clutch Pos, Steering %, "
                "Steering Wheel Position (deg), Steering Shaft Torque (N.m), FFB Output, Engine RPM, Gear, Lap Number, "
                "Lap Distance, tyre temps/pressures/wear, brake temps, ride heights, GPS (local coords)",
    "hz": "20 (speed, pedals, steering, torque, rpm, gear); 100 (lap number, session time, FFB); 5 (lap distance, timing)",
    "laps": 9,
    "best_lap": "54.0 s (9 complete laps 29-37: 54-56 s each; lap 28 66 s and lap 38 16 s are partial)",
    "input_device": "wheel (high confidence: force-feedback channels Steering Shaft Torque and FFB Output present)",
    "wheel_rotation_deg": "recorded: Steering Wheel Position, range -63.2 to +139.0 deg; wheel lock setting not stated",
    "game_version": "not recorded (rFactor 2; DAMPlugin logging per repo README)",
    "date": "2025-08-03 16:34:45 (from header)",
    "author": "not stated (nickname only in source)",
    "license": "not stated (no LICENSE file in repo)",
    "access": "free",
    "downloaded": "no: raw not kept (header has a driver-name field); derived in derived/rf2_matsusaka_p1/",
    "sha256": LD_SHA256 + " (.ld); ldx " + LDX_SHA256,
    "verified": "yes",
    "notes": "not LMU; use only as rF2 fallback reference; speed/throttle/brake/rpm plausibility checked (0-241 km/h, 0-100 %, 0-7794 rpm); "
             "Steering % channel has asymmetric range (-25..55), use Steering Wheel Position deg",
})

# Sources that were checked but hold no downloadable LMU wheel data (kept so nobody re-searches them)
SOURCE_ROWS = [
    ("LMU", "Local LMU telemetry files (UserData\\Telemetry .duckdb/.ld/.csv)", "https://lemansultimate.wiki.gg/wiki/Telemetry", "local files of the player", "free", "Local to the game owner's PC; no public copy found; wiki blocked from this sandbox."),
    ("LMU", "pavva94/LMUTelemetry (reads LMU native DuckDB)", "https://github.com/pavva94/LMUTelemetry", "GitHub repo", "free", "add_repo: not found or no access; not read. Would show native DuckDB schema if accessible."),
    ("LMU", "Coach Dave Academy Delta (telemetry + reference laps)", "https://coachdaveacademy.com/product/le-mans-ultimate-setup-subscription/", "paid subscription", "paid", "Paid (GBP 11.99/mo or GBP 109/yr). Not bought. Site blocked from sandbox."),
    ("LMU", "LMU Trace (lap sharing, cloud accounts)", "https://lmutrace.com/", "online service", "paid", "Subscription from EUR 2.50/mo after trial per snippet. Not registered."),
    ("LMU", "Track Titan (LMU via plugin; bundle lists recorded data)", "https://intercom.help/track-titan/it/articles/6227990-quali-giochi-sono-supportati-da-track-titan", "paid service", "paid", "Support for v1.4 unconfirmed. Not registered."),
    ("LMU", "Overtake.gg Telemetry Tool for LMU", "https://overtake.gg/downloads/telemetry-tool-for-lmu.73664", "tool download", "login", "Download needs account. Blocked from sandbox. Tool, not a dataset."),
    ("LMU", "Garage61 (LMU support and public laps)", "", "online service", "login", "LMU support not confirmed by any source found; site not reached. Not registered."),
    ("LMU", "Reddit / r/LeMansUltimate lap-sharing threads", "https://www.reddit.com/r/LeMansUltimate/", "forum", "free", "Blocked from sandbox (403). Search returned no thread with lap files."),
    ("LMU", "Overtake.gg / LMU community forum telemetry threads", "https://www.overtake.gg/", "forum", "free", "Blocked from sandbox (403); community.lemansultimate.com unreachable."),
    ("LMU", "Steam discussions and guides (app 2399420)", "https://store.steampowered.com/app/2399420/", "store page", "free", "Blocked (403); app id from a steamcommunity link in search results."),
    ("LMU", "Kaggle / Zenodo / Hugging Face / Figshare / Mendeley / OSF (LMU)", "https://www.kaggle.com", "dataset hubs", "free", "No LMU telemetry dataset in search results; hosts blocked (403)."),
    ("unknown", "Hugging Face dda71427/train.json (speed, steering angle, throttle, brake)", "https://huggingface.co/datasets/dda71427/train.json", "dataset file", "free", "Game and card unknown; host blocked (403); not checked."),
    ("Project CARS (not LMU, not in fallback list)", "Univ. of Luxembourg 2017 driving study (25 participants, one circuit)", "https://vehicularlab.uni.lu/publication/faye2017poster/faye2017poster.pdf", "poster; dataset offer", "free", "Host blocked (403). Brake channel and download unconfirmed."),
    ("none (real driving, not racing)", "IEEE DataPort 'Driving simulator data' (Ohio State, DOI 10.21227/wp1p-3v65)", "https://ieee-dataport.org/documents/driving-simulator-data", "dataset", "free", "Host blocked. Not racing; pedal force used as brake proxy."),
    ("synthetic (not human)", "Learn-to-Race (arXiv 2103.11575, MPC experts)", "https://arxiv.org/pdf/2103.11575", "paper + dataset", "free", "Expert laps from a controller, not people. arXiv blocked."),
    ("synthetic (not human)", "SimLingo CARLA raw set (Hugging Face)", "https://huggingface.co/datasets/TESS-Computer/carla-simlingo-raw", "dataset", "free", "Controls from PDM-Lite rule expert. Not human data. Host blocked."),
    ("AMS2", "sim-to-motec test fixtures ams2_idle/inrace/inpits.bin (24 KB each)", "https://github.com/GeekyDeaks/sim-to-motec", "binary test snapshots", "free", "Short shared-memory fragments, not laps. Not decoded (verified no)."),
    ("ACC", "decnet100/acr_telemetry motec/Sample.ld", "https://github.com/decnet100/acr_telemetry", "MoTeC sample", "free", "Real car (MoTeC M800 ECU channels, 2005, 'Belgrave'), not a sim: excluded."),
    ("iRacing", "libibt / @hotlap.ai/telemetry packages", "https://pypi.org/project/libibt/", "parser libraries", "free", "Code only, no .ibt sample inside (checked sdist and npm tarball listings). No public iRacing laps found."),
    ("AMS2 / other", "Overtake AVUS (Reiza) and other AMS2 telemetry tools", "https://forum.reizastudios.com/threads/announcing-avus.35535/", "tools", "login", "Tools that record your own laps; no public dataset found."),
    ("LMU", "Novapool/hack_the_track (ml_data CSVs)", "https://github.com/Novapool/hack_the_track", "GitHub repo", "free", "Aggregated per-stint features, not raw telemetry; game not stated. Headers only."),
    ("LMU", "Herbertmt978/MoTeC-MCP", "https://github.com/Herbertmt978/MoTeC-MCP", "GitHub repo", "free", "add_repo: not found or no access; not read."),
    ("none", "LMU-Tracking-Desktop/tracker git history (prisma/dev.db versions)", "https://github.com/LMU-Tracking-Desktop/tracker/commits", "git history", "free", "3 older DB versions (20-22 laps with telemetry); all lap IDs already in HEAD: no extra data."),
]
for game, name, url, fmt, access, note in SOURCE_ROWS:
    rows.append({
        "track": "n/a (source)", "layout": "", "car": "", "class": "", "game": game,
        "source_url": url, "file_url": "", "format": fmt, "channels": "", "hz": "", "laps": 0,
        "best_lap": "", "input_device": "unknown", "wheel_rotation_deg": "", "game_version": "",
        "date": "", "author": "not stated", "license": "", "access": access, "downloaded": "no",
        "sha256": "", "verified": "no", "notes": f"{name}: {note}",
    })

with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLUMNS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in COLUMNS})
print("rows:", len(rows), "| lmu laps:", sum(1 for r in rows if r["game"] == "LMU" and r["laps"] == 1),
      "| rf2 rows:", sum(1 for r in rows if r["game"].startswith("rF2")))
