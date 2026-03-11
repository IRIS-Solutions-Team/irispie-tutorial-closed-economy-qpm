r"""
Read US data from St Louis Fred database
"""


import macrotap as mt
import irispie as ir
import file_structure as fs


# Download raw data from Fred

fred_db = mt.from_fred(["GDPC1", "CPIAUCSL", "TB3MS"])


# Convert monthly to quarterly

fred_db["CPIAUCSL"].fill_missing(method="log_linear", )
fred_db["CPIAUCSL"].aggregate(ir.QUARTERLY, method="mean", )
fred_db["TB3MS"].aggregate(ir.QUARTERLY, method="mean", )


# Create model-consistent databox

historical_db = ir.Databox()
historical_db["y"] = 100 * ir.log(fred_db["GDPC1"])
historical_db["cpi"] = 100 * ir.log(fred_db["CPIAUCSL"])
historical_db["rs" ] = fred_db["TB3MS"]


# Save to a CSV data file

historical_db.to_csv_file(fs.HISTORICAL_DATA_FILE, )

