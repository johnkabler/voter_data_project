import pandas, redactometer, grid_search

def test_boolean():
    testing = pandas.DataFrame.from_csv('../data/test_dark.csv', sep="\t")
    training = pandas.DataFrame.from_csv('../data/train_dark.csv', sep="\t")

    param_grid = {'min_width_ratio': [0.01, 0.05, 0.10, 0.20], 
                'max_width_ratio': [0.80, 0.85, 0.90, 0.95], 
                'min_height_ratio': [0.01, 0.05, 0.10, 0.20],
                'max_height_ratio': [0.80, 0.85, 0.90, 0.95]} 
    #train
    params, score = grid_search.gridsearch(param_grid, training, '../train_dark/', 'is_censored')

    #test
    results = [(p, grid_search.eval(testing, p, '../train_dark/', 'is_censored')) for p in params]

    return results


def test_count():
    testing = pandas.DataFrame.from_csv('../data/test_dark.csv', sep="\t")
    training = pandas.DataFrame.from_csv('../data/train_dark.csv', sep="\t")

    param_grid = {'min_width_ratio': [0.01, 0.02, 0.3, 0.04, 0.05], 
                'max_width_ratio': [0.80, 0.85, 0.90], 
                'min_height_ratio': [0.10, 0.20],
                'max_height_ratio': [0.80, 0.85, 0.90]} 

    #train
    params, score = grid_search.gridsearch(param_grid, training, '../train_dark/', 'total_censor')

    #test
    results = [(p, grid_search.eval(testing, p, '../train_dark/', 'total_censor')) for p in params]
    
    return results


score, correct = grid_search.count_scoring(train, '../train_dark/', 
				{'min_width_ratio': 0.05, 
                'max_width_ratio': 0.9, 
                'min_height_ratio': 0.05,
                'max_height_ratio': 0.9} )