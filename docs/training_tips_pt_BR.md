Instruções e dicas para o treinamento RVC
======================================
Essas DICAS explicam como o treinamento de dados é feito.

# Fluxo de treinamento
Explicarei ao longo das etapas na guia de treinamento da GUI.

## Passo1
Defina o nome do experimento aqui.

Você também pode definir aqui se o modelo deve levar o tom em consideração.
Se o modelo não considerar o tom, o modelo será mais leve, mas não adequado para cantar.

Os dados para cada experimento são colocados em`/logs/your-experiment-name/`.

## etapa2a
Carrega e pré-processa áudio.

### Carregar Áudio
Se você especificar uma pasta com áudio, os arquivos de áudio nessa pasta serão lidos automaticamente.
Por exemplo, se você especificar `C:Users\hoge\voices`, `C:Users\hoge\voices\` voice.mp3 será carregado, mas `C:Users\hoge\voices\dir\voice.mp3` não será carregado.

Como o ffmpeg é usado internamente para ler áudio, se a extensão for suportada pelo ffmpeg, ela será lida automaticamente.
Depois de converter para int16 com ffmpeg, converta para float32 e normalize entre -1 para 1.

### Removendo ruído
O áudio é suavizado pelo filtfilt do scipy.

### Divisão de Áudio
Primeiro, o áudio de entrada é dividido pela detecção de partes do silêncio que duram mais do que um determinado período (max_sil_kept=5 segundos?). Depois de dividir o áudio em silêncio, divida o áudio a cada 4 segundos com uma sobreposição de 0,3 segundos. Para áudio separado em 4 segundos, depois de normalizar o volume, converta o arquivo wav para`/logs/your-experiment-name/0_gt_wavs` e, em seguida, converta-o para 16k taxa de amostragem para`/logs/your-experiment-name/1_16k_wavs ` como um arquivo wav.

## etapa2b
### Extrair passo
Extrair informações de pitch dos arquivos wav. Extraia as informações de pitch (=f0) usando o método embutido em parselmouth ou pyworld e salve-as em`/logs/your-experiment-name/2a_f0`. Em seguida, converta logaritmicamente as informações de tom para um número inteiro entre 1 e 255 e salve-as em`/logs/your-experiment-name/2b-f0nsf`.

### Extrair feature_print
Converta o arquivo WAV para incorporação com antecedência usando o HuBERT. Leia o arquivo WAV salvo em`/logs/your-experiment-name/1_16k_wavs`, converta o arquivo WAV em recursos de 256 dimensões com o HuBERT e salve no formato npy em`/logs/your-experiment-name/3_feature256`.

## Passo3
treine o modelo.
### Glossário para iniciantes
Na aprendizagem profunda, o conjunto de dados é dividido e a aprendizagem prossegue pouco a pouco. Em uma atualização de modelo (etapa), os dados batch_size são recuperados e as previsões e correções de erros são realizadas. Fazer isso uma vez para um conjunto de dados conta como uma época.

Portanto, o tempo de aprendizado é o tempo de aprendizado por etapa x (o número de dados no tamanho do conjunto de dados / lote) x o número de épocas. Em geral, quanto maior o tamanho do lote, mais estável o aprendizado se torna (tempo de aprendizado por etapa ÷ tamanho do lote) se torna menor, mas usa mais memória GPU. A RAM da GPU pode ser verificada com o comando nvidia-smi. O aprendizado pode ser feito em um curto espaço de tempo, aumentando o tamanho do lote, tanto quanto possível, de acordo com a máquina do ambiente de execução.

### Informar modelo pré-treinado
O RVC começa a treinar o modelo a partir de pesos pré-treinados em vez de 0, para que possa ser treinado com um pequeno conjunto de dados.

Por padrão

- Se você considerar o pitch, ele `carrega rvc-location/pretrained/f0G40k.pth` e `rvc-location/pretrained/f0D40k.pth`.
- Se você não considerar o pitch, ele carrega `rvc-location/pretrained/f0G40k.pth` e `rvc-location/pretrained/f0D40k.pth`.

Ao aprender, os parâmetros do modelo são salvos em `logs/your-experiment-name/G_{}.pth` e `logs/your-experiment-name/D_{}.pth` para cada save_every_epoch, mas especificando esse caminho, você pode começar a aprender. Você pode reiniciar ou começar a treinar a partir de pesos modelo aprendidos em um experimento diferente.

### índice de aprendizagem
O RVC salva os valores de recursos do HuBERT usados durante o treinamento e, durante a inferência, procura valores de recursos semelhantes aos valores de recursos usados durante o aprendizado para realizar a inferência. Para realizar essa pesquisa em alta velocidade, o índice é aprendido com antecedência.
Para o aprendizado de índice, usamos a biblioteca de pesquisa aproximada de vizinhança faiss. Leia o valor do recurso `logs/your-experiment-name/3_`feature256 e use-o para aprender o índice e salve-o como `logs/your-experiment-name/add_XXX.index`.

(A partir da versão de atualização 20230428, ele é lido a partir do índice, e salvar / especificar não é mais necessário.)

### Descrição do botão
- Modelo do trem: Após executar a etapa 2b, pressione este botão para treinar o modelo.
- Índice de características do trem: Após treinar o modelo, realize o aprendizado do índice.
- Treinamento com um clique: etapa 2b, treinamento de modelo e treinamento de índice de recursos de uma só vez.