import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoCartaCorrecao
from pynfe.entidades.fonte_dados import _fonte_dados

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = ''
uf = 'MT'
homologacao = True
CPFCNPJ = ''
chave = ''
protocolo = ''


carta_correcao = EventoCartaCorrecao(
    cnpj=CPFCNPJ,  # cnpj do emissor
    chave=chave,  # chave de acesso da nota
    data_emissao=datetime.datetime.now(),
    uf=uf,
    n_seq_evento=1,
    correcao='Texto livre'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe_cc = serializador.serializar_evento(carta_correcao)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe_cc)

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.evento(modelo='nfe', evento=xml)  # modelo='nfce' ou 'nfe'
print(envio.text)
