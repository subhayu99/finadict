# 📈 FINAnce preDICT

**FINADICT** is an interactive **Streamlit** web app that leverages **yFinance**, **FB Prophet**, **Plotly** and **Streamlit** to fetch, visualize, and forecast market data for **stocks**, **forex**, and **cryptocurrencies**; all packaged in a single **Docker** image. Users can select financial instruments, time intervals, and historical ranges to generate:

* 📈 **Live and historical visualizations** (line and candlestick charts)
* 🔮 **Next-day/hour price predictions** with confidence intervals using Facebook Prophet
* 📥 **Downloadable CSV reports** for raw and predicted data
* 📉 **Forecast accuracy metrics** like Mean Accuracy and RMSPE

---

## 🚧 Note from the Author

This project was originally built as a **learning experience** to explore time-series forecasting, financial APIs, and full-stack deployment.

🧠 I ran it live on `finadict.tech` for a year to gain hands-on experience with hosting and maintaining a web app.

💸 However, due to the recurring **domain and hosting costs**, it's **no longer actively hosted** or maintained on any live server.

You're welcome to run it locally or self-host it using the instructions below!

---

## 🛠 Installation

### 🐧 On Linux (Debian/Ubuntu)

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python3-pip
git clone https://github.com/subhayu99/finadict.git
cd finadict
pip3 install -r requirements.txt
streamlit run app.py
````

---

### 🐳 Run in Docker

#### ▶ Using Prebuilt Docker Image

```bash
sudo docker run -d -i --name finadict -h finadict -p 80:80 -e STREAMLIT_SERVER_PORT=80 subhayu99/finadict:latest
```

#### ▶ Build from Dockerfile

```bash
mkdir finadict && cd finadict
wget https://raw.githubusercontent.com/subhayu99/finadict/main/Dockerfile
sudo docker build -t subhayu99/finadict:latest .
sudo docker run -d -i --name finadict -h finadict -p 80:80 -e STREAMLIT_SERVER_PORT=80 subhayu99/finadict:latest
```

#### ▶ Using docker-compose

```bash
mkdir finadict && cd finadict
wget https://raw.githubusercontent.com/subhayu99/finadict/main/docker-compose.yaml
sudo docker-compose up -d
```

---

## 📸 Screenshots

### 1. Stock’s Raw Data Table

<p align="center"><img src="Screenshot/1.png" alt="Raw Data Table" width="70%"/></p>

### 2. Historical Price Graph

<p align="center"><img src="Screenshot/2.png" alt="Raw Data Graph" width="70%"/></p>

### 3. Forecasted Prices

<p align="center"><img src="Screenshot/3.png" alt="Forecast Table" width="70%"/></p>

### 4. Forecast Plot

<p align="center"><img src="Screenshot/4.png" alt="Forecast Plot" width="70%"/></p>

---

## 👨‍💻 Contributors

Thanks to all the contributors who made this project possible!

🔗 See [Contributors.md](https://github.com/subhayu99/finadict/blob/master/Contributors.md) for more info.
📊 GitHub Contributions: [Graph](https://github.com/subhayu99/finadict/graphs/contributors)

---

> 💡 Built with ❤️ out of curiosity, to learn and experiment with real-world finance data.
