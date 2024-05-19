# 🔎 Welcome to ViGPT Researcher

This repository was inspired by the [ViGPTQA](https://aclanthology.org/2023.emnlp-industry.70), [Plan-and-Solve](https://arxiv.org/abs/2305.04091), and [RAG](https://arxiv.org/abs/2005.11401) papers. The goal is to create a chatbot for Vietnamese people, which can answer questions and solve problems in various domains. ViGPT Researcher was expected to generate high-quality responses with accurate, unbiased, factual, and real-time information by leveraging the power of LLMs and the knowledge from the Internet.

## Issues
1. *OSError: cannot load library 'gobject-2.0-0': gobject-2.0-0: cannot open shared object file*:
    - **Solution**: `conda install -c anaconda pango` prior to `pip install weasyprint` works, but that's unfortunate that there is no pure pip solution where all project dependencies can be pip installed from a requirements file.

2. Maybe you also get this error: *error: subprocess-existed-with-error/metadata-generation-failed*:
    - **Solution**: Let's try these steps. I'm not sure that they will also solve your issue!
  
   ```
       python -m pip install -U pip
       python -m pip install -U setuptools wheel
       python -m pip install [package] --no-build-isolation
   ```

3. The problem relates to the CUDA version (*These instructions worked with Ubuntu:*):
   * Update:
   ```
       sudo apt update
   ```
   * Install CUDA:
   ```
      sudo apt install [cuda version you want]
   ```
   * Find where CUDA is installed:
   ```
       ls /usr/local/
   ```
   * Update environment variables:
   ```
       export PATH=/usr/local/cuda-version/bin${PATH:+:${PATH}}
       export LD_LIBRARY_PATH=/usr/local/cuda-version/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
       echo 'export PATH=/usr/local/cuda-version/bin${PATH:+:${PATH}}' >> ~/.bashrc
       echo 'export LD_LIBRARY_PATH=/usr/local/cuda-version/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
   ```
   * Now, let's check CUDA:
   ```
       ncvv -V
   ```
   It will show CUDA as the installed version.
   
#### Importance: You should follow the instructions on your work, such as the terminal before seeking the solutions outside if you do not understand your problem!
