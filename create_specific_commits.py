import datetime
import subprocess

# Specific dates user worked on (corrected - Feb has 28 days in 2026)
work_dates = [
    # February
    (2026, 2, 23), (2026, 2, 26), (2026, 2, 28),
    # March
    (2026, 3, 4), (2026, 3, 5), (2026, 3, 12), (2026, 3, 17), (2026, 3, 20), (2026, 3, 25),
    # April
    (2026, 4, 14), (2026, 4, 17), (2026, 4, 21), (2026, 4, 24),
    # May
    (2026, 5, 7), (2026, 5, 8), (2026, 5, 21), (2026, 5, 22),
    # June
    (2026, 6, 9), (2026, 6, 23),
    # July
    (2026, 7, 16), (2026, 7, 23),
    # August
    (2026, 8, 6), (2026, 8, 7), (2026, 8, 13), (2026, 8, 27), (2026, 8, 28),
]

dates = [datetime.datetime(y, m, d, 10, 0, 0) for y, m, d in work_dates]
dates.sort()

print(f"Creating {len(dates)} commits on specific work dates")

# Add all files
subprocess.run(["git", "add", "-A"], check=True)

# Create first commit
date_str = dates[0].strftime("%Y-%m-%d %H:%M:%S")
subprocess.run(["git", "commit", "--date", date_str, "-m", "update"], check=True)
print(f"✓ Commit 1 on {date_str}")

# Create empty commits for remaining dates
for i, date in enumerate(dates[1:], 2):
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "--allow-empty", "--date", date_str, "-m", "update"], check=True)
    print(f"✓ Commit {i} on {date_str}")

print(f"\nAll {len(dates)} commits created!")
subprocess.run(["git", "log", "--oneline"], check=True)
