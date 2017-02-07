import sleuth_automation as slaut


def test_param_interpolation_satans_flavor():
    satans_params = {'diff': 666,
                     'diff_start': 666,
                     'diff_step': 666,
                     'diff_end': 666,
                     'brd': 666,
                     'brd_start': 666,
                     'brd_step': 666,
                     'brd_end': 666,

                     'sprd': 666,
                     'sprd_start': 666,
                     'sprd_step': 666,
                     'sprd_end': 666,

                     'slp': 666,
                     'slp_start': 666,
                     'slp_step': 666,
                     'slp_end': 666,

                     'rg': 666,
                     'rg_start': 666,
                     'rg_step': 666,
                     'rg_end': 666 }

    s = slaut.Location('Group22', '/path/i', '/path/o', 2001, 2060, [1980,1990,2000])
    with open('tests/satans.scenario') as f:
        assert s.create_scenario_file(satans_params, 666) == f.read()
