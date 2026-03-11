r"""
Simulate a forecast
"""

import sys
import irispie as ir
import file_structure as fs


model = ir.Simultaneous.from_pickle_file(fs.MODEL_PICKLE_FILE, )
filter_db = ir.Databox.from_csv_file(fs.FILTER_DATA_FILE, )

history_end = ir.qq(2022,4)
forecast_start = history_end + 1
forecast_end = history_end + 4*4
forecast_span = forecast_start >> forecast_end
chart_span = forecast_start-12 >> forecast_end

steady_db = model.build_steady_paths(chart_span, )

s0 = model.simulate(
    filter_db, forecast_span,
)

ch = ir.Chartpack(
    tiles=(3,3),
    span=chart_span,
    highlight=forecast_span,
    legend=["Forecast", "Steady state", ],
)

f = ch.add_figure("Forecast", )
f.add_charts([
    "Output, Q/Q PA: ad_y",
    "Potential output, Q/Q PA: ad_y_tnd",
    "Output gap, %: y_gap",
    "CPI, Q/Q PA: ad_cpi",
    "Nominal interest rate: rs",
    "Real interest rate: rrs",
])

chart_db = ir.Databox.by_merging([s0, steady_db, ])

ch.plot(chart_db, )

