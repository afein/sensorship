From    hypriot/rpi-python 

RUN apt-get update && apt-get install -y python-pygame

COPY    . /src

EXPOSE  1234 
EXPOSE  1235
CMD     ["python", "-u", "/src/server.py"]
