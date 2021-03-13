FROM wlserver1/ytupload:latest
ADD ./ /
RUN python3 views.py