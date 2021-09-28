# FINAnce preDICT

A simple and easy to use Stocks / Cryptocurreny / Foreign Exchange prices predictor.

## Live website : [finadict.tech](https://finadict.tech/)


## Installion

### On Linux 

> **Ubuntu / Debian**

```bash
sudo apt-get update && apt-get upgrade
sudo apt-get install python3-pip
git clone https://github.com/subhayu99/finadict.git
cd finadict
sudo pip3 install -r requirements.txt
streamlit run app.py
```

### On a docker container

> **Using docker image**

```bash
sudo docker pull subhayu99/finadict:latest .
sudo docker run -d -i --name finadict -h finadict -p 80:80 -e STREAMLIT_SERVER_PORT=80 subhayu99/finadict:latest
```

> **Using Dockerfile**

```bash
mkdir finadict && cd finadict
wget https://raw.githubusercontent.com/subhayu99/finadict/main/Dockerfile
sudo docker build -t subhayu99/finadict:latest .
sudo docker run -d -i --name finadict -h finadict -p 80:80 -e STREAMLIT_SERVER_PORT=80 subhayu99/finadict:latest
```

> **Using docker-compose**

```bash
mkdir finadict && cd finadict
wget https://raw.githubusercontent.com/subhayu99/finadict/main/compose.yaml
sudo docker-compose up -d
```

