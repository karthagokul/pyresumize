FROM python:3.9
# Or any preferred Python version.
ADD test_pip_module.py .
RUN pip install pyresumize
#CMD [“python”, “apps/text_file.py”]
#docker exec -it <mycontainer> bash