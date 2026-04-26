# ====================
# Stage 1: builder
# ====================
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements_hf.txt .
RUN pip install --user --no-cache-dir -r requirements_hf.txt

# ====================
# Stage 2: final
# ====================
FROM python:3.12-slim

WORKDIR /app

# Copiar los paquetes instalados desde el builder
COPY --from=builder /root/.local /root/.local

# Copiar el código fuente
COPY . .

# Asegurar que los scripts instalados con pip estén en el PATH
ENV PATH=/root/.local/bin:$PATH

# Puerto por defecto de Streamlit (si se usara como dashboard)
EXPOSE 8501

# Comando por defecto: ejecuta el bot en modo simulación
CMD ["python", "-m", "ai_mastery.cli", "bot", "--cv-file", "cv.txt", "--keyword", "python", "--location", "Madrid"]