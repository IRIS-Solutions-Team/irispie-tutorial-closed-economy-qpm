
import sys
import irispie as ir


m = ir.Simultaneous.from_pickle_file("model.pkl", )


start_sim = ir.ii(1)
end_sim = ir.ii(40)
sim_span = start_sim >> end_sim
chart_span = start_sim-1 >> end_sim

d = m.build_steady_paths(sim_span, )
d["shk_y_gap"][start_sim>>start_sim+3] = -2

s0, info0 = m.simulate(
    d, sim_span,
    return_info=True,
)

s1, info1 = m.simulate(
    d, sim_span,
    return_info=True,
    method="stacked_time",
    solver_settings={"step_tolerance": 1, },
)

s = ir.Databox.by_merging((s0, s1), )

ch = ir.Chartpack(span=chart_span, )
fig = ch.add_figure("Adverse demand shock")
fig.add_charts((
    "Output gap: y_gap",
    "Inflation: ad_cpi",
    "Interest rate: rs",
    "Unconstrained interest rate: rs_unc",
))

ch.plot(s, )

