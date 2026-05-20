"""Homework solution for data manipulation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT_DIR / "files" / "input"
OUTPUT_DIR = ROOT_DIR / "files" / "output"
PLOTS_DIR = ROOT_DIR / "files" / "plots"


def generate_outputs() -> pd.DataFrame:
	"""Create summary table and top-10 plot from input data."""

	drivers_path = INPUT_DIR / "drivers.csv"
	timesheet_path = INPUT_DIR / "timesheet.csv"

	drivers = pd.read_csv(drivers_path)
	timesheet = pd.read_csv(timesheet_path)

	totals = (
		timesheet.groupby("driverId", as_index=False)
		.agg({"hours-logged": "sum", "miles-logged": "sum"})
		.rename(columns={"hours-logged": "total_hours", "miles-logged": "total_miles"})
	)

	summary = drivers.merge(totals, on="driverId", how="left").fillna(0)

	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	summary_path = OUTPUT_DIR / "summary.csv"
	summary.to_csv(summary_path, index=False)

	top10 = summary.sort_values("total_miles", ascending=False).head(10)
	PLOTS_DIR.mkdir(parents=True, exist_ok=True)
	plot_path = PLOTS_DIR / "top10_drivers.png"

	plt.figure(figsize=(10, 6))
	plt.barh(top10["name"], top10["total_miles"])
	plt.gca().invert_yaxis()
	plt.title("Top 10 Drivers by Miles")
	plt.xlabel("Total Miles")
	plt.tight_layout()
	plt.savefig(plot_path)
	plt.close()

	return summary


if __name__ == "__main__":
	generate_outputs()