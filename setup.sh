#!/bin/bash

mkdir -p ~/.streamlit/
printf "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
