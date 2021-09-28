# finadict

A simple and easy to use Stocks / Cryptocurreny / Foreign Exchange prices predictor.

## Available on [finadict.tech](finadict.tech)

## To run it locally

### On Linux ( Ubuntu )

```bash
apt-get update && apt-get upgrade
apt-get install python3-pip
git clone https://github.com/subhayu99/finadict.git
cd finadict
pip3 install -r requirements.txt
streamlit run app.py
```
### Using Docker

#### Using Dockerfile

```bash
docker build -t subhayu99/finadict:latest .
docker run -d -i --name finadict -h finadict -p 80:80 -e STREAMLIT_SERVER_PORT=80 subhayu99/finadict:latest
```

#### Using docker-compose

```bash
docker-compose up -d
```

