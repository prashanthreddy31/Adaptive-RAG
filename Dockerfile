# Stage 1 : builder
FROM python:3.11-slim AS builder

WORKDIR /builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.11-slim AS runtime

RUN groupadd -r appgroup && useradd -r -g  appgroup -d /app appuser

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local


# Copy both services into the image
COPY src/ ./src/
COPY streamlit_app/ ./streamlit_app/

RUN chown -R appuser:appgroup /app

USER appuser

# Default target — overridden per-service in docker-compose.yml
ARG SERVICE=backend
ENV SERVICE=${SERVICE}

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD if [ "$SERVICE" = "backend" ]; then \
          curl -f http://localhost:8000/docs || exit 1; \
        else \
          curl -f http://localhost:8501/_stcore/health || exit 1; \
        fi
 
CMD ["sh", "-c", \
     "if [ \"$SERVICE\" = \"backend\" ]; then \
        uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2; \
      else \
        streamlit run streamlit_app/home.py --server.port 8501 --server.address 0.0.0.0; \
      fi"]