FROM python:3.6

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install nano vim
RUN apt-get -y install git
RUN apt-get -y install python3-pydot python-pydot python-pydot-ng graphviz
RUN apt-get -y install python3-tk
RUN apt-get -y install zip unzip

RUN pip install pyvis networkx==2.2 matplotlib numpy ciso8601 pyarrow==0.13.0 lxml graphviz pandas scipy scikit-learn pytz==2018.9 lime joblib
RUN pip install pydotplus bpmn_python==0.0.18
RUN pip install keras tensorflow joblib

RUN pip install pulp ortools
COPY . /app
RUN cd /app && cp tests/test_dockers/setups/setup_predictionIntegration.py setup.py && python setup.py install
