
nvidia-smi -L
pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html
git clone https://github.com/NVIDIA/apex
pip install -r requirements.txt
pip install unidecode
python train.py --output_directory=outdir --log_directory=logdir