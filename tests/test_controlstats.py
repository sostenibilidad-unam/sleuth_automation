from sleuth_automation.controlstats import ControlStats

def test_params_right_start_and_step_trivial_1s():
    cs = ControlStats('tests/control_stats.log_1s', 1)

    assert cs.params == {'brd': 1,
                         'brd_end': 4,
                         'brd_start': 0,
                         'brd_step': 1,
                         'diff': 1,
                         'diff_end': 4,
                         'diff_start': 0,
                         'diff_step': 1,
                         'rg': 1,
                         'rg_end': 4,
                         'rg_start': 0,
                         'rg_step': 1,
                         'slp': 1,
                         'slp_end': 4,
                         'slp_start': 0,
                         'slp_step': 1,
                         'sprd': 1,
                         'sprd_end': 4,
                         'sprd_start': 0,
                         'sprd_step': 1}

    cs = ControlStats('tests/control_stats.log_1s', 5)

    assert cs.params ==  {'brd': 1,
                          'brd_end': 20,
                          'brd_start': 0,
                          'brd_step': 5,
                          'diff': 1,
                          'diff_end': 20,
                          'diff_start': 0,
                          'diff_step': 5,
                          'rg': 1,
                          'rg_end': 20,
                          'rg_start': 0,
                          'rg_step': 5,
                          'slp': 1,
                          'slp_end': 20,
                          'slp_start': 0,
                          'slp_step': 5,
                          'sprd': 1,
                          'sprd_end': 20,
                          'sprd_start': 0,
                          'sprd_step': 5}



def test_params_right_start_and_step_trivial_100s():
    cs = ControlStats('tests/control_stats.log_100s', 5)

    assert cs.params == {'brd': 100,
                         'brd_end': 100,
                         'brd_start': 80,
                         'brd_step': 5,
                         'diff': 100,
                         'diff_end': 100,
                         'diff_start': 80,
                         'diff_step': 5,
                         'rg': 100,
                         'rg_end': 100,
                         'rg_start': 80,
                         'rg_step': 5,
                         'slp': 100,
                         'slp_end': 100,
                         'slp_start': 80,
                         'slp_step': 5,
                         'sprd': 100,
                         'sprd_end': 100,
                         'sprd_start': 80,
                         'sprd_step': 5}
    cs = ControlStats('tests/control_stats.log_100s', 1)

    assert cs.params == {'brd': 100,
                         'brd_end': 100,
                         'brd_start': 96,
                         'brd_step': 1,
                         'diff': 100,
                         'diff_end': 100,
                         'diff_start': 96,
                         'diff_step': 1,
                         'rg': 100,
                         'rg_end': 100,
                         'rg_start': 96,
                         'rg_step': 1,
                         'slp': 100,
                         'slp_end': 100,
                         'slp_start': 96,
                         'slp_step': 1,
                         'sprd': 100,
                         'sprd_end': 100,
                         'sprd_start': 96,
                         'sprd_step': 1}



def test_params_right_start_and_step_25_100():
    cs = ControlStats('tests/control_stats.log_25_100', 5)

    assert cs.params == {'brd': 25,
                         'brd_end': 97,
                         'brd_start': 25,
                         'brd_step': 18,
                         'diff': 25,
                         'diff_end': 97,
                         'diff_start': 25,
                         'diff_step': 18,
                         'rg': 25,
                         'rg_end': 97,
                         'rg_start': 25,
                         'rg_step': 18,
                         'slp': 25,
                         'slp_end': 97,
                         'slp_start': 25,
                         'slp_step': 18,
                         'sprd': 25,
                         'sprd_end': 97,
                         'sprd_start': 25,
                         'sprd_step': 18}
