
    !transition-variables

        y, y_tnd, diff_y_tnd
        y_gap
        diff_cpi, diff4_cpi, E_diff_cpi
        rs
        rrs_gap
        rrs
        cpi


    % !shocks

        % ant_shk_y_gap, ant_shk_diff_cpi, ant_shk_rs


    !shocks

        shk_y_tnd, shk_y_gap, shk_diff_cpi, shk_rs, shk_E_diff_cpi


    !parameters

        ss_rrs, ss_diff_cpi, ss_diff_y_tnd
        c0_y_gap, c1_y_gap
        c0_diff_cpi, c1_diff_cpi
        c1_E_diff_cpi
        c0_rs, c1_rs
        c0_y_tnd


    !transition-equations

        y = y_tnd + y_gap;

        diff(y_tnd) = diff_y_tnd/4;

        diff_y_tnd = ss_diff_y_tnd + shk_y_tnd;
        % y_tnd = c0_y_tnd * y_tnd{-1} + shk_y_tnd;

        y_gap = ...
            + c0_y_gap * y_gap{-1} ...
            - c1_y_gap * rrs_gap ...
            ... + ant_shk_y_gap ...
            + shk_y_gap ...
        !! y_gap = 0;

        diff_cpi = ...
            + c0_diff_cpi * diff_cpi{-1} ...
            + (1 - c0_diff_cpi) * E_diff_cpi ...
            + c1_diff_cpi * y_gap ...
            ... + ant_shk_diff_cpi ...
            + shk_diff_cpi ...
        !! diff_cpi = ss_diff_cpi;

        E_diff_cpi = ...
            + c1_E_diff_cpi * diff_cpi{+1} ...
            + (1 - c1_E_diff_cpi) * ss_diff_cpi ...
            + shk_E_diff_cpi ...
        !! E_diff_cpi = ss_diff_cpi;

        rs = ...
            + c0_rs * rs{-1} ...
            + (1 - c0_rs)*(ss_rrs + ss_diff_cpi + c1_rs*(diff4_cpi{+3} - ss_diff_cpi)) ...
            ... + ant_shk_rs ...
            + shk_rs ...
        !! rs = ss_rrs + ss_diff_cpi;

        rrs = rs - diff_cpi{+1};

        rrs_gap = rrs - ss_rrs;

        diff4_cpi = (diff_cpi + diff_cpi{-1} + diff_cpi{-2} + diff_cpi{-3})/4;

        diff(cpi) = diff_cpi/4;


    !measurement-variables

        obs_y
        obs_y_gap
        obs_y_gap4
        obs_rs
        obs_cpi


    !measurement-equations

        obs_y = y;
        obs_y_gap = y_gap;
        obs_y_gap4 = y_gap{-4};
        obs_rs = rs;
        obs_cpi = cpi;

