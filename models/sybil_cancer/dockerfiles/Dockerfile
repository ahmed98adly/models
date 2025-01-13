FROM mhubai/base:latest

# install and system lybraries and dependencies
# install model 

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install torch==1.13.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install torchvision==0.14.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install git+https://github.com/reginabarzilaygroup/Sybil.git

RUN buildutils/download_weights.sh \
    ~/.sybil/src/checkpoints \
    https://github.com/reginabarzilaygroup/Sybil/releases/download/v1.0.3/sybil_checkpoints.zip 
    

ENV WEIGHTS_DIR="/root/.cache/torch/hub/checkpoints/"
ENV WEIGHTS_URL="https://download.pytorch.org/models/r3d_18-b3b3357e.pth"
ENV WEIGHTS_FN="r3d_18-b3b3357e.pth" 

RUN wget --directory-prefix ${WEIGHTS_DIR} ${WEIGHTS_URL}

# specify entrypoint
ENTRYPOINT ["mhub.run"]
CMD ["--config", "/app/models/sybil_cancer/config/default.yml"]