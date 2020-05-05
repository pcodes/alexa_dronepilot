FROM python:3

ADD alexa_skill.py /
ADD v9.py /

ENTRYPOINT ["python","-u","./alexa_skill.py"]
CMD []
