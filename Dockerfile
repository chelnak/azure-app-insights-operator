FROM python:3.8
ADD ./operator /operator
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD kopf run /operator/app_insights_operator.py --verbose --priority 100