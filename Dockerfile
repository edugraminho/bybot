# Use uma imagem Python base
FROM python:3.10-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina as variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Espere por arquivos de dependência
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Execute o script no contêiner
CMD ["sh", "run.sh"]
