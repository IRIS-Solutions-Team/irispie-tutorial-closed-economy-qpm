
# Import packages
import irispie as ir

# Load model object
model = ir.Simultaneous.from_pickle_file("pickle_files/model.pkl")

# Load historical data from Kalman filter
db = ir.Databox.from_csv_file("data_files/filter_data.csv")

# Simulate model
hist_end = ir.qq(2025,4)
fcast_start = hist_end + 1
fcast_end = hist_end + 5*4
fcast_span = fcast_start >> fcast_end

fcast_db = model.simulate(
    db, fcast_span,
)

# Chart results

ch = ir.Chartpack(
    tiles=(3, 3),
    span = hist_end-20 >> fcast_end,
    highlight=fcast_span,
)

f = ch.add_figure("Forecast")
f.add_chart("CPI, Q/Q PA: ad_cpi")
f.add_chart("Interest rate: rs")
f.add_chart("Output gap: y_gap")
f.add_chart("Output, Q/Q PA: ad_y")
f.add_chart("Real interest rate: rrs")

ch.plot(fcast_db)