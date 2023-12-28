# paddle_ocr_service
PaddleOCRService base on paddleOCR and Flask

## Requirement

```shell
conda create --name ppocr python=3.9 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda activate ppocr
conda env remove --name ppocr
```

Due to the requirement install error of PyMuPDF<1.21.0 at Mac M1 Chip, 
the requirements.txt install paddleocr~=2.6 first,
then using the following command to upgrade and resolve requirement conflict:

```shell
pip install -r requirements.txt && pip install -U "paddleocr~=2.7" --no-deps
```