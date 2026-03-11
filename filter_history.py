r"""
Run Kalman filter on the historical data, and set up initial conditions for the forecast
"""


import sys
import irispie as ir
import file_structure as fs


model = ir.Simultaneous.from_pickle_file(fs.MODEL_PICKLE_FILE, )

model.assign_strict(
    std_shk_rs=3,
    std_shk_ad_cpi=1,
    std_shk_rrs_tnd=0.5,
)

model.check_steady()
model.solve_first_order()


hist_db = ir.Databox.from_csv("hist_data.csv", )

obs_db = hist_db.copy(
    source_names=("y", "rs", "cpi", ),
    target_names=lambda n: f"obs_{n}",
)

start_filt = ir.qq(2010,1)
end_filt = ir.qq(2022,4)
filter_span = start_filt >> end_filt

multiplier_db = ir.Databox(
    std_shk_obs_cpi=ir.Series(periods=ir.qq(2022,1)>>ir.qq(2022,4), values=0, )
)

std_db = ir.Databox(
    std_shk_rs=10,
    std_shk_ad_y_tnd=ir.Series(periods=ir.qq(2019,3)>>ir.qq(2021,1), values=10, )
)

tv_stds = model.vary_stds(
    multiplier_db=multiplier_db,
    #std_db=std_db,
    std_db=None,
    span=filter_span,
)

kalman_db, info, = model.kalman_filter(
    obs_db, filter_span,
    return_info=True,
    rescale_variance=True,
)

s0 = kalman_db["smooth_med"]
s0["filter_span"] = ir.Series(periods=filter_span, values=1, )
s0.to_csv_file(fs.FILTER_DATA_FILE, )

sys.exit()


filt_db, info, = model.kalman_filter(
    obs_db, filter_span,
    return_info=True,
    rescale_variance=True,
    prepend_initial=True,
)
s1 = filt_db["smooth_med"]

s = filt_db["smooth_med"]

tv_filt_db, tv_info = model.kalman_filter(
    obs_db | tv_stds, filter_span,
    return_info=True,
    rescale_variance=True,
    stds_from_data=True,
)

tv_s = tv_filt_db["smooth_med"]


std_scale = info["std_scale"]
m_rescaled = model.copy()
m_rescaled.rescale_stds(std_scale, )

_, info_rescaled = m_rescaled.kalman_filter(
    obs_db, filter_span,
    return_info=True,
    rescale_variance=True,
)

