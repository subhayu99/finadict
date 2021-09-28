FROM subhayu99/fbprophet

LABEL maintainer="Subhayu Kumar Bala ( balasubhayu99@gmail.com )"

RUN apt-get update
RUN git clone https://github.com/subhayu99/finadict.git

WORKDIR /root/notebooks/finadict

RUN pip3 install -r requirements.txt

ENV STREAMLIT_SERVER_PORT 80

EXPOSE 80

STOPSIGNAL SIGTERM

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
