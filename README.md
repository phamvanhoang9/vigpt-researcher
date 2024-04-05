# 🔎 Welcome to VIGPT Researcher

This repository was inspired by the [ViGPTQA](https://aclanthology.org/2023.emnlp-industry.70), [Plan-and-Solve](https://arxiv.org/abs/2305.04091), and [RAG](https://arxiv.org/abs/2005.11401) papers. The goal is to create a chatbot for Vietnamese people, which can answer questions and solve problems in various domains. VIGPT Researcher was expected to generate high-quality responses with accurate, unbiased, factual, and real-time information by leveraging the power of LLMs and the knowledge from the Internet.

## Issues
1. *OSError: cannot load library 'gobject-2.0-0': gobject-2.0-0: cannot open shared object file*:
    - **Solution for Ubuntu**: `conda install -c anaconda pango` prior to `pip install weasyprint` works, but that's unfortunate that there is no pure pip solution where all project dependencies can be pip installed from a requirements file.
