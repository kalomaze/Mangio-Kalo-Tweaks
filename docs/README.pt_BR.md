<div align="center">

<h1>Retrieval-based-Voice-Conversion-WebUI</h1>
Uma estrutura de conversão de voz fácil de usar baseada em VITS.<br><br>

[![madewithlove](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI)

<img src="https://counter.seku.su/cmoe?name=rvc&theme=r34" /><br>

[![Open In Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/github/liujing04/Retrieval-based-Voice-Conversion-WebUI/blob/main/Retrieval_based_Voice_Conversion_WebUI.ipynb)
[![Licença](https://img.shields.io/github/license/liujing04/Retrieval-based-Voice-Conversion-WebUI?style=for-the-badge)](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI/blob/main/%E4%BD%BF%E7%94%A8%E9%9C%80%E9%81%B5%E5%AE%88%E7%9A%84%E5%8D%8F%E8%AE%AE-LICENSE.txt)
[![Huggingface](https://img.shields.io/badge/🤗%20-Spaces-yellow.svg?style=for-the-badge)](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

[![Discord](https://img.shields.io/badge/RVC%20Developers-Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/HcsmBBGyVk)

</div>

------
[**Changelog**](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI/blob/main/Changelog_CN.md) | [**FAQ (Perguntas Frequentes)**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/FAQ-(Frequently-Asked-Questions))

[**Inglês**](./README.en.md) | [**中文简体**](../README.md) | [**日本語**](./README.ja.md) | [**한국어**](./README.ko.md) ([**韓國語**](./README.ko.han.md))


Confira nosso [vídeo de demonstração](https://www.bilibili.com/video/BV1pm4y1z7Gm/) aqui!

Software de conversão de voz em tempo real usando RVC[: w-okada/voice-changer](https://github.com/w-okada/voice-changer)

> Uma demonstração online usando RVC que converte áudio vocal em guitarra acústica:https://huggingface.co/spaces/lj1995/vocal2guitar

> Vídeo de demonstração doVocal2Guitar ：https://www.bilibili.com/video/BV19W4y1D7tT/

> O conjunto de dados para o modelo de pré-treinamento usa quase 50 horas de conjunto de dados de código aberto VCTK de alta qualidade.

> Conjuntos de dados de música licenciados de alta qualidade serão adicionados ao conjunto de treinamento um após o outro para seu uso, sem se preocupar com violação de direitos autorais.

## Resumo
Este repositório tem as seguintes características:
+ Reduza o vazamento de tom substituindo o recurso de origem pelo recurso de conjunto de treinamento usando a recuperação top1;
+ Treinamento fácil e rápido, mesmo em placas gráficas relativamente pobres;
+ Treinamento com uma pequena quantidade de dados também obtém resultados relativamente bons (>=10min de fala de baixo ruído recomendado);
+ Apoiando a fusão de modelos para alterar timbres (usando ckpt processing tab- >ckpt merge);
+ Interface Webui fácil de usar;
+ Use o modelo UVR5 para separar rapidamente vocais e instrumentos.
## Preparar o ambiente
Recomendamos que você instale as dependências através da poesia.

Os seguintes comandos precisam ser executados no ambiente do Python versão 3.8 ou superior:
```bash
# Install PyTorch-related core dependencies, skip if installed
# Reference: https://pytorch.org/get-started/locally/
pip install torch torchvision torchaudio

#For Windows + Nvidia Ampere Architecture(RTX30xx), you need to specify the cuda version corresponding to pytorch according to the experience of https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI/issues/21
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

# Install the Poetry dependency management tool, skip if installed
# Reference: https://python-poetry.org/docs/#installation
curl -sSL https://install.python-poetry.org | python3 -

# Install the project dependencies
poetry install
```
Você também pode usar o pip para instalar as dependências

```bash
pip install -r requirements.txt
```

## Preparação de outros pré-modelos
RVC requer outros pré-modelos para inferir e treinar.

Você precisa baixá-los do nosso [espaço Huggingface](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/).

Aqui está uma lista de pré-modelos e outros arquivos que o RVC precisa:
```bash
hubert_base.pt

./pretrained

./uvr5_weights

If you want to test the v2 version model (the v2 version model has changed the input from the 256 dimensional feature of 9-layer Hubert+final_proj to the 768 dimensional feature of 12-layer Hubert, and has added 3 period discriminators), you will need to download additional features

./pretrained_v2

#If you are using Windows, you may also need this dictionary, skip if FFmpeg is installed
ffmpeg.exe
```
Em seguida, use este comando para iniciar o Webui:
```bash
python infer-web.py
```
Se você estiver usando o Windows, poderá baixar e extrair o `RVC-beta.7z` para usar o RVC diretamente e usar o `go-web.bat` para iniciar o Webui.

Há também um tutorial sobre RVC em chinês e você pode verificar se necessário.

## Créditos
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)
+ [Removedor Vocal Ultimate](https://github.com/Anjok07/ultimatevocalremovergui)
+ [cortador de áudio](https://github.com/openvpi/audio-slicer)
## Agradecemos a todos os colaboradores por seus esforços

<a href="https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=liujing04/Retrieval-based-Voice-Conversion-WebUI" />
</a>

