# Voice Separator - Separação de Vocais com IA

Uma aplicação web simples e eficiente para separar elementos de áudio (vocais, bateria, baixo, outros instrumentos) de músicas usando inteligência artificial.

## 🎵 O que faz

- **Separar vocais** da música de fundo (karaoke)
- **Extrair instrumentos** individualmente (bateria, baixo, outros)
- **Processar vídeos do YouTube** automaticamente
- **Interface web fácil** - sem necessidade de programação
- **Múltiplos formatos** - aceita MP3, WAV, FLAC, M4A, AAC

## 🚀 Como usar

### Opção 1: Docker (Recomendado - Mais Fácil)

**Super simples - apenas um comando:**

```bash
# Método mais simples (arquivos salvos dentro do container)
docker run -d -p 7860:7860 --name voice-separator paladini/voice-separator

# Método recomendado (arquivos acessíveis no seu computador)
git clone https://github.com/paladini/voice-separator-demucs.git
cd voice-separator-demucs
docker compose up -d
```

Acesse: http://localhost:7860

**Pronto!** Se usar o segundo método, seus arquivos aparecerão na pasta `output/`.

### Opção 2: Instalação Manual

**Pré-requisitos:**
- Python 3.8 ou superior
- FFmpeg instalado no sistema

**Instalar FFmpeg:**

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS (com Homebrew)
brew install ffmpeg

# Windows: baixe de https://ffmpeg.org/download.html
```

**Configurar o projeto:**

```bash
# 1. Entrar na pasta do projeto
cd voice-separator-demucs

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python main.py
```

Acesse: http://localhost:7860

## 🎯 Como usar a interface
### Seleção de Modelo de IA

Agora é possível escolher entre diferentes modelos de IA para separação:

- **Demucs CPU Lite (mdx_extra_q):** Mais rápido, funciona em qualquer CPU (padrão).
- **Demucs v3 (mdx):** Rápido, GPU recomendada para melhor desempenho.
- **Demucs v4 (htdemucs):** Velocidade média, requer GPU.
- **Demucs HD (htdemucs_ft):** Melhor qualidade, requer GPU.

**Como funciona:**
- Por padrão, o modelo mais rápido (Demucs CPU Lite) é usado em todas as separações.
- Para escolher outro modelo, habilite a opção "Seleção de modelo" na interface web. Isso mostrará um menu para selecionar o modelo desejado.
- Se a opção não estiver habilitada, a seleção de modelo fica oculta e o modelo padrão é utilizado.

**Dica:** Se você não possui GPU, selecione Demucs CPU Lite para melhor compatibilidade e velocidade.

### Upload de Arquivo
1. **Selecione quais elementos extrair** (vocais, bateria, baixo, etc.)
2. **Escolha um arquivo de áudio** do seu computador
3. **Clique em "Separar"**
4. **Aguarde o processamento** (2-5 minutos dependendo do arquivo)
5. **Baixe os resultados** em MP3

### YouTube
1. **Selecione quais elementos extrair**
2. **Cole a URL do vídeo** (ex: https://www.youtube.com/watch?v=...)
3. **Clique em "Baixar e Separar"**
4. **Aguarde download + processamento**
5. **Baixe os arquivos separados**

**Limitações do YouTube:**
- Máximo 10 minutos de duração
- Apenas vídeos públicos
- Funciona melhor com vídeos musicais

## 🎛️ Tipos de separação

- **� Vocais** - Voz principal da música
- **🎹 Instrumental** - Música completa sem vocais (para karaoke)
- **🥁 Bateria** - Apenas a percussão
- **🎸 Baixo** - Linha de baixo isolada  
- **🎵 Outros** - Demais instrumentos (guitarra, piano, etc.)

## ⏱️ Tempo de processamento

- **1 elemento** (ex: só vocais): ~2-3 minutos
- **2 elementos** (ex: vocal + instrumental): ~3-4 minutos
- **Todos os elementos**: ~4-6 minutos

*Tempos podem variar conforme o hardware do seu computador*

## 📥 Como baixar os arquivos

**Se usou o método simples (sem pasta output):**
```bash
# Copiar arquivos do container para seu computador
docker cp voice-separator:/app/static/output ./meus-arquivos/
```

**Se usou o método recomendado:**
- Os arquivos já estão na pasta `output/` do seu computador!

## 📋 Formatos aceitos

- **MP3** - Mais comum
- **WAV** - Alta qualidade
- **FLAC** - Audio sem perda
- **M4A** - iTunes/Apple
- **AAC** - Comprimido

**Tamanho máximo:** Sem limite de tamanho de arquivo (uso local)

### 🎧 Suporte a Canais de Áudio

A aplicação agora suporta **arquivos WAV mono** com conversão automática para estéreo:

- **Arquivos mono (1 canal):** Convertidos automaticamente para estéreo duplicando o canal
- **Arquivos estéreo (2 canais):** Processados diretamente sem conversão
- **Arquivos multi-canal:** Convertidos para estéreo para compatibilidade

**Como funciona:**
1. O sistema detecta o número de canais de áudio no seu arquivo
2. Se mono for detectado, converte automaticamente para estéreo
3. A conversão mantém a qualidade e taxa de amostragem
4. O processamento continua normalmente com o arquivo estéreo
5. Arquivos temporários de conversão são limpos automaticamente

**Benefícios:**
- Não é necessário converter arquivos mono manualmente
- Processamento transparente de vários formatos de áudio
- Mantém a qualidade original do áudio
- Funciona com todos os formatos de áudio suportados

## 🔧 Solução de problemas

### "Erro ao carregar modelo"
- Aguarde alguns minutos na primeira execução
- O modelo de IA é baixado automaticamente (~200MB)
- Verifique sua conexão com a internet

### "FFmpeg não encontrado"
Instale o FFmpeg no seu sistema:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Processamento muito lento
- Use um computador com mais RAM (recomendado: 8GB+)
- Feche outros programas pesados
- Use arquivos menores (menos de 10 minutos)

### Vídeo do YouTube não funciona
- Verifique se o vídeo é público
- Máximo 10 minutos de duração
- Alguns vídeos podem ter restrições de download

## 🧠 Tecnologia

Esta aplicação usa o **Demucs**, um modelo de inteligência artificial desenvolvido pelo Facebook/Meta AI especificamente para separação de fontes musicais. É baseado em redes neurais profundas treinadas em milhares de músicas.

## � Precisa de ajuda?

Se encontrar problemas:
1. Leia a seção "Solução de problemas" acima
2. Verifique se o FFmpeg está instalado
3. Teste com um arquivo pequeno primeiro
4. Reinicie a aplicação se necessário

## 📝 Nota sobre uso

Esta ferramenta é destinada para uso pessoal e educacional. Respeite os direitos autorais das músicas que você processar.

## 👨‍💻 Desenvolvido por

**Fernando Paladini** ([@paladini](https://github.com/paladini))

Baseado no modelo Demucs do Facebook/Meta AI Research.

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.
