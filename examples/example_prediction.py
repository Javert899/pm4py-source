import os

from pm4py.algo.prediction import factory as prediction_factory
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.log import EventLog


def execute_script():
    log_path = os.path.join("..", "tests", "input_data", "running-example.xes")
    log = xes_importer.apply(log_path)
    train_log = EventLog(log[2:6])
    test_log = EventLog(log[0:2])

    # train and test Elasticnet model
    model1 = prediction_factory.train(train_log)
    prediction_factory.save(model1, "model1.dump")
    del model1
    model1 = prediction_factory.load("model1.dump")
    os.remove("model1.dump")
    pred_res1 = prediction_factory.test(model1, test_log)
    print("PREDICTION RESULT ELASTICNET = ")
    print(pred_res1)
    del model1

    # train and test Keras-RNN model
    model2 = prediction_factory.train(train_log, variant="keras_rnn")
    prediction_factory.save(model2, "model2.dump")
    del model2
    model2 = prediction_factory.load("model2.dump")
    os.remove("model2.dump")
    pred_res2 = prediction_factory.test(model2, test_log)
    print("PREDICTION RESULT KERAS = ")
    print(pred_res2)
    del model2


if __name__ == "__main__":
    execute_script()
