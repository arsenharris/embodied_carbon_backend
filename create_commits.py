import datetime
import subprocess

# Start date: Feb 8, 2026 (Sunday)
start_date = datetime.datetime(2026, 2, 8, 10, 0, 0)
end_date = datetime.datetime(2026, 8, 29, 10, 0, 0)

# Generate weekend dates (Saturdays and Sundays)
current_date = start_date
dates = []

while current_date <= end_date:
    # Check if it's Saturday (5) or Sunday (6)
    if current_date.weekday() in [5, 6]:
        dates.append(current_date)
    current_date += datetime.timedelta(days=1)

print(f"Creating {len(dates)} commits on weekends from Feb 8 to Aug 29")

# First, add all files
subprocess.run(["git", "add", "-A"], check=True)

# Create initial commit with first date
date_str = dates[0].strftime("%Y-%m-%d %H:%M:%S")
subprocess.run(["git", "commit", "--date", date_str, "-m", "update"], check=True)
print(f"✓ Commit 1 on {date_str}")

# For remaining dates, we'll create empty commits
for i, date in enumerate(dates[1:], 2):
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    # Allow empty commits
    subprocess.run(["git", "commit", "--allow-empty", "--date", date_str, "-m", "update"], check=True)
    print(f"✓ Commit {i} on {date_str}")

print(f"\nAll {len(dates)} commits created!")
subprocess.run(["git", "log", "--oneline"], check=True)
