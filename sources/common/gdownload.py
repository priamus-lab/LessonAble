import gdown
def gdownload(id, output):
    d = 'https://drive.google.com/uc?id='
    gdown.download(d+id, output, quiet=False);