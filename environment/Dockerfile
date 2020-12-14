# hash:sha256:e6381da41acb91cbcf9c2c03b5bc10167bd89638c0ece4c661d80c218b3ec953
FROM registry.codeocean.com/codeocean/miniconda3:4.8.2-python3.8-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN conda install -y \
        jupyter==1.0.0 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    pyyaml==5.3.1 \
    seaborn==0.11.0 \
    xlsxwriter==1.3.7
