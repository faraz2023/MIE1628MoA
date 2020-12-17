# Reference: https://github.com/interviewstreet/spark-stratifier

import itertools
import numpy as np

from pyspark import since, keyword_only
from pyspark.ml import Estimator, Model
from pyspark.ml.common import _py2java
from pyspark.ml.param import Params, Param, TypeConverters
from pyspark.ml.param.shared import HasSeed
from pyspark.ml.tuning import CrossValidator, CrossValidatorModel
from pyspark.ml.util import *
from pyspark.ml.wrapper import JavaParams
from pyspark.sql.functions import rand
from functools import reduce
from multiprocessing.pool import ThreadPool

class StratifiedCrossValidator(CrossValidator):
  def stratify_data(self, dataset):
    """
    Returns an array of dataframes with the same ratio of passes and failures.

    Currently only supports binary classification problems.
    """

    epm = self.getOrDefault(self.estimatorParamMaps)
    numModels = len(epm)
    nFolds = self.getOrDefault(self.numFolds)
    split_ratio = 1.0 / nFolds

    passes = dataset[dataset['label'] == 1]
    fails = dataset[dataset['label'] == 0]

    pass_splits = passes.randomSplit([split_ratio for i in range(nFolds)])
    fail_splits = fails.randomSplit([split_ratio for i in range(nFolds)])
    for i in range(len(pass_splits)):
      one_count_train = pass_splits[i].count()
      zero_count_train = fail_splits[i].count()
      factor = zero_count_train/one_count_train
      if factor > 2:
        fail_splits[i] = fail_splits[i].sample(fraction = 0.5, withReplacement = False,  seed = 42) 
        
        pass_splits[i]  = pass_splits[i].sample(fraction = factor, withReplacement = True,  seed = 42)
        
        
#         pass_splits[i] = spark.createDataFrame(pass_splits[i].toPandas().sample(n = fail_splits[i].count(), replace = True,  random_state = 0))
    
    
    stratified_data = [pass_splits[i].unionAll(fail_splits[i]) for i in range(nFolds)]

    return stratified_data

  def _fit(self, dataset):
    est = self.getOrDefault(self.estimator)
    epm = self.getOrDefault(self.estimatorParamMaps)
    numModels = len(epm)
    eva = self.getOrDefault(self.evaluator)
    nFolds = self.getOrDefault(self.numFolds)
    seed = self.getOrDefault(self.seed)
    metrics = [0.0] * numModels
    
    stratified_data = self.stratify_data(dataset)
    
    for i in range(nFolds):
      train_arr = [x for j,x in enumerate(stratified_data) if j != i]
      train = reduce((lambda x, y: x.unionAll(y)), train_arr)
      validation = stratified_data[i]

      models = est.fit(train, epm)

      for j in range(numModels):
        model = models[j]
        metric = eva.evaluate(model.transform(validation, epm[j]))
        metrics[j] += metric/nFolds

    if eva.isLargerBetter():
      bestIndex = np.argmax(metrics)
    else:
      bestIndex = np.argmin(metrics)

    bestModel = est.fit(dataset, epm[bestIndex])
    return self._copyValues(CrossValidatorModel(bestModel, metrics))