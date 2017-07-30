# docker run -p 5000:5000 -p 8000:8000 crap
FROM paulinus/opensfm-docker-base

COPY . /source/crap-OpenSfM

WORKDIR /source/crap-OpenSfM

RUN pip install -r requirements.txt && \
    python setup.py build

EXPOSE 5000
EXPOSE 8000
ENV FLASK_APP run.py
RUN mkdir -p /source/crap-OpenSfM/uploads/images
CMD ["python", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
