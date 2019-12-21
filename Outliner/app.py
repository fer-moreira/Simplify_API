from core.engine import PageReader
import sys
import codecs

def main ():
    reader = PageReader()

    # reader.url = 'https://oglobo.globo.com/esportes/zico-exclusivo-quero-ver-torcida-feliz-nao-estou-preocupado-se-vao-lembrar-de-mim-24148095'
    # reader.url = 'https://www.nytimes.com/2019/12/20/us/mitch-mcconnell-impeachment-strategy.html'
    # reader.url = 'https://www1.folha.uol.com.br/poder/2019/12/primeiro-alvo-de-hackers-foi-eduardo-bolsonaro-diz-relatorio-da-pf.shtml'
    # reader.url = 'https://economia.estadao.com.br/noticias/geral,odebrecht-demite-marcelo-odebrecht-acionista-e-ex-presidente-do-grupo,70003132823'
    # reader.url = 'https://www.wired.com/story/facebook-removes-accounts-ai-generated-photos/'

    # dump_json = reader.dump_json
    dump_html = reader.dump_html

    file = codecs.open('debug.html','w','utf-8')
    file.write(str(dump_html))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting (Ctrl + c)")
        sys.exit()