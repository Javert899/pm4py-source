cd python35
docker build --no-cache -t testdockerlinuxpython35bpmnintegration .
docker run testdockerlinuxpython35bpmnintegration bash -c "cd pm4py-source-bpmnIntegration2/tests && python execute_tests.py"
docker run testdockerlinuxpython35bpmnintegration bash -c "python -c \"import pm4py ; print(pm4py.__version__)\""
cd ..
cd python37
docker build --no-cache -t testdockerlinuxpython37bpmnintegration .
docker run testdockerlinuxpython37bpmnintegration bash -c "cd pm4py-source-bpmnIntegration2/tests && python execute_tests.py"
docker run testdockerlinuxpython37bpmnintegration bash -c "python -c \"import pm4py ; print(pm4py.__version__)\""
cd ..
cd python36
docker build --no-cache -t testdockerlinuxpython36bpmnintegration .
docker run testdockerlinuxpython36bpmnintegration bash -c "cd pm4py-source-bpmnIntegration2/tests && python execute_tests.py"
docker run testdockerlinuxpython36bpmnintegration bash -c "python -c \"import pm4py ; print(pm4py.__version__)\""
