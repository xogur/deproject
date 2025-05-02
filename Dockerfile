FROM apache/airflow:2.10.5

USER root

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libdrm2 \
    libxshmfence1 \
    libgbm1 \
    --no-install-recommends

# ✅ Chrome 설치
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/114.0.5735.90/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm chrome-linux64.zip

# ✅ ChromeDriver 설치
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

USER airflow

# ✅ Python 패키지 설치
RUN pip install --no-cache-dir \
    selenium \
    requests \
    beautifulsoup4 \
    pandas \
    pyperclip \
    opencv-python \
    scikit-learn \
    matplotlib \
    pycryptodome \
    flask-cors # 🔐 AES 복호화용 패키지 추가

# ❌ argparse 제거 (Airflow 내부 충돌 방지)
RUN pip uninstall -y argparse

