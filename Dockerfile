FROM python:3.10-alpine AS compile-image

RUN apk --no-cache add gcc musl-dev python3-dev g++
RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --user --no-cache-dir --upgrade -r /code/requirements.txt

COPY src /code/src

FROM python:3.10-alpine AS build-image

RUN mkdir /code
RUN addgroup -S appuser && adduser -S appuser -G appuser

RUN chown -R appuser /code

USER appuser

ENV PYTHONPATH=.
ENV PATH=/home/appuser/.local/bin:$PATH

COPY --from=compile-image /root/.local/ /home/appuser/.local/
COPY --from=compile-image /code /code/

WORKDIR /code

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
