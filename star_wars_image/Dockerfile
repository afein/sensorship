From    hypriot/rpi-python 
COPY    . /src

RUN apt-get update && apt-get install python-pygame

EXPOSE  1234 
EXPOSE  1235
CMD     ["python", "-u", "/src/server.py"]
