FROM python:3.14

RUN addgroup coder
RUN useradd -g coder coder

COPY . /home/coder/coder-core
WORKDIR /home/coder

RUN pip install -e coder-core[test]

# Download wait-for-it to allow waiting for dependency containers
RUN mkdir util
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > util/wait-for-it.sh
RUN chmod +x util/wait-for-it.sh

WORKDIR /home/coder/coder-core

ENTRYPOINT ["pytest", "--cov=codercore", "-n", "logical", "-q", "--cov-report", "term-missing"]
