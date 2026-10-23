FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HF_HOME=/app/data/hf-cache HF_HUB_CACHE=/app/data/hf-cache/hub
COPY pyproject.toml requirements.txt ./
COPY core ./core
COPY loaders ./loaders
COPY chunkers ./chunkers
COPY embedders ./embedders
COPY stores ./stores
COPY retrievers ./retrievers
COPY llms ./llms
COPY api ./api
COPY cli ./cli
COPY evaluation ./evaluation
COPY projects ./projects
COPY agents ./agents
COPY web ./web
COPY samples ./samples
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]
