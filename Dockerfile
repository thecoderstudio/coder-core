FROM python:3.11

RUN addgroup coder
RUN useradd -g coder coder

COPY . /home/coder/coder-core
WORKDIR /home/coder

RUN pip install -e coder-core[test]

WORKDIR /home/coder/coder-core

ENTRYPOINT ["pytest", "--cov=codercore", "-q", "--cov-report", "term-missing"]
