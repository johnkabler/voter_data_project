"""
Grid Search this is thus far for dark censors
"""
import redactometer
import pandas
import itertools
import time
import numpy as np

def gridsearch(param_grid, train, img_root, metric, censor_type="dark"):
    """Lorem Ipsum"""
    #no cross-val simple param setting
    train = train[train.redaction_type == censor_type]

    combos = [{key: value for (key, value) in zip(param_grid, values)} 
             for values in itertools.product(*param_grid.values())]

    #I believe this is not the efficient way. (Dataframes should not be iterated)

    max_score = 0
    argmax = []  
    print "number combos", len(combos)

    for combo in combos:
        #boolean
        if metric == 'is_censored':
            score = boolean_scoring(train, img_root, combo)

        #are we able to get the right number of blobs?
        if metric == 'total_censor':
            score = count_scoring(train, img_root, combo)

        #update
        if score >= max_score:
            max_score = score
            argmax.append(combo) 
    return argmax, max_score     

def complete_search(training, img_dir, metric, min_start, min_stop, max_start, max_stop, step):
    #range is inclusive
    min_range = np.arange(min_start, min_stop, step)
    max_range = np.arange(max_start, max_stop, step)
    param_grid = {'min_width_ratio' : min_range,
                'max_width_ratio': max_range,
                'min_height_ratio': mirn_range,
                'max_height_ratio': max_range}
    return gridsearch(param_grid, training, img_dir, metric)

def boolean_scoring(data, url, params):
    """does not filter by censor type yet"""
    correct = sum((len(redactometer.censor_dark(url + i, **params)[1]) > 0) \
       == data.ix[i]['is_censored'] for i in data.index)
    score = float(correct)/float(len(data.index))
    return score

def count_scoring_binary(data, url, params):
    """Returns correct only if entire document correct"""
    correct = sum(len(redactometer.censor_fill(url + i, **params)[1]) \
                == data.total_censor[i] for i in data.index)
    results = [(i, len(redactometer.censor_fill(url + i, **params)[1]), data.total_censor[i]) \
                    for i in data.index]

    score = float(correct)/float(len(data.index))
    return score, results
 

def count_scoring(data, url, params):
    """Count number of censors detected over real number""" 
    error = np.mean([abs_error(len(redactometer.censor_fill(url + i, **params)[1]), \
              data.total_censor[i]) for i in data.index])
    return 1 - error


def blurred_count_scoring(data, url, aperture):
    """Count number of censors detected over real number, aperture default 25""" 
    error = np.mean([abs_error(len(redactometer.blurred_detection(url + i, aperture)[0]), \
              data.total_censor[i]) for i in data.index])
    return 1 - error


def f_score(data, url, params):
    predicted = float(sum([len(redactometer.censor_fill(url + i, **params)[1]) \
                    for i in data.index]))
    truepos = float(sum([len(redactometer.censor_fill(url + i, **params)[1]) \
                 == data.total_censor[i] for i in data.index]))
    #verify by coordinate! Above not correct. Truepos = relevant ^ retrieved


    precision = truepos / predicted
    recall = truepos / sum(data.total_censor)

    F = 2 * (precision * recall) / (precision + recall)

    return F

def eval(data, url, params):
    """ return score and individual metrics"""
    score = count_scoring(data, url, params)
    
    metrics = [(i, len(redactometer.censor_fill(url + i, **params)[1]),  data.total_censor[i], \
                    abs_error(len(redactometer.censor_fill(url + i, **params)[1]), \
                    data['total_censor'][i])) for i in data.index]
        
    metrics = pandas.DataFrame(metrics, columns=['img', 'observed', 'actual', 'error'])
    #scores.to_csv(outfile, sep="\t")

    return score, metrics


def abs_error(observed, actual):
    return abs(float(actual - observed) / float(actual))





