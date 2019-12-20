from core.engine import PageReader
import sys
from pprint import pprint

def main ():
    reader = PageReader()
    reader.url = 'https://oglobo.globo.com/esportes/zico-exclusivo-quero-ver-torcida-feliz-nao-estou-preocupado-se-vao-lembrar-de-mim-24148095'
    # reader.url = 'https://www1.folha.uol.com.br/poder/2019/12/ex-governador-ricardo-coutinho-e-preso-sob-suspeita-de-desvio-de-verba-na-paraiba.shtml'

    dump_json = reader.dump_json

    pprint(dump_json)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting (Ctrl + c)")
        sys.exit()