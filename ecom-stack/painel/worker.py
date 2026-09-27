"""Worker isolado do Homefy. Execute com: python -m painel.worker"""
from . import trabalhos

if __name__ == "__main__":
    trabalhos.worker_forever()
