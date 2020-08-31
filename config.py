start_year = 1980
end_year = 2019

adv_stat_attrs = ['ws', 'vorp', 'ts_pct']
not_to_compare = ['name', 'age', 'year', 'ws', 'mp_per_g', 'mvp_score', 'g']
per_game_stat_attrs = ['g', 'age', 'pts_per_g', 'trb_per_g', 'ast_per_g', 'stl_per_g',
                       'blk_per_g',
                       'tov_per_g', 'mp_per_g', 'fg_pct']

modification_rules = {'ignore': ['mvp_score'], 'all': ['g', 'ws', 'vorp', 'age', 'mp_per_g'], 'fg_pct': ['pts_per_g'],
                      'ts_pct': ['pts_per_g'], 'tov_per_g': ['ast_per_g']}

output_feature = 'mvp_score'
