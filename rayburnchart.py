import re
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


# Official Texas Water Development Board reservoir data
url = (
    "https://waterdatafortexas.org/"
    "reservoirs/individual/sam-rayburn-30day.csv"
)

# Download the CSV directly into pandas
df = pd.read_csv(url)


# -----------------------------------
# Clean the column names
# -----------------------------------

def clean_column_name(name):
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


df.columns = [clean_column_name(c) for c in df.columns]

print("Columns received from Water Data for Texas:")
print(df.columns.tolist())


# -----------------------------------
# Find the important columns
# -----------------------------------

date_col = next(
    (
        c for c in df.columns
        if "date" in c or "timestamp" in c
    ),
    None
)

level_col = next(
    (
        c for c in df.columns
        if "water_level" in c
    ),
    None
)

if level_col is None:
    level_col = next(
        (
            c for c in df.columns
            if "elevation" in c
            and "pool" not in c
        ),
        None
    )

if level_col is None:
    level_col = next(
        (
            c for c in df.columns
            if "level" in c
            and "pool" not in c
        ),
        None
    )

percent_col = next(
    (
        c for c in df.columns
        if "percent" in c and "full" in c
    ),
    None
)


if date_col is None or level_col is None:
    raise ValueError(
        f"Could not identify date/water-level columns. "
        f"Available columns: {df.columns.tolist()}"
    )


# -----------------------------------
# Prepare the data
# -----------------------------------

df[date_col] = pd.to_datetime(
    df[date_col],
    errors="coerce"
)

df[level_col] = pd.to_numeric(
    df[level_col],
    errors="coerce"
)

df = (
    df.dropna(subset=[date_col, level_col])
      .sort_values(date_col)
)


# -----------------------------------
# Create the chart
# -----------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    df[date_col],
    df[level_col],
    marker="o",
    markersize=4
)

plt.title(
    "Sam Rayburn Reservoir — 30-Day Water Level"
)

plt.xlabel("Date")
plt.ylabel("Water Level (ft)")

plt.grid(alpha=0.3)

plt.gcf().autofmt_xdate()

plt.tight_layout()

plt.savefig(
    "sam_rayburn_30day_level.png",
    dpi=150
)

plt.close()


# -----------------------------------
# Create a latest-status text file
# -----------------------------------

latest = df.iloc[-1]

summary = [
    f"Latest reading: {latest[date_col].date()}",
    f"Water level: {latest[level_col]:.2f} ft"
]

if percent_col is not None:
    percent_value = pd.to_numeric(
        latest[percent_col],
        errors="coerce"
    )

    if pd.notna(percent_value):
        summary.append(
            f"Percent full: {percent_value:.1f}%"
        )


with open("sam_rayburn_latest.txt", "w") as file:
    file.write("\n".join(summary))


print("Sam Rayburn chart successfully created.")
