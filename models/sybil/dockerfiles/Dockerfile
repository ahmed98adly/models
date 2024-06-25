FROM mhubai/base:latest

# install and system lybraries and dependencies
# install model 
RUN pip install torch==1.13.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install torchvision==0.14.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install git+https://github.com/reginabarzilaygroup/Sybil.git

# load model definition
ARG MHUB_MODELS_REPO
RUN buildutils/import_mhub_model.sh sybil ${MHUB_MODELS_REPO}

# specify entrypoint
ENTRYPOINT ["mhub.run"]
CMD ["--config", "/app/models/sybil/config/default.yml"]
