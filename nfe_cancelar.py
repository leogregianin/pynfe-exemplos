import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoCancelarNota
from pynfe.entidades.fonte_dados import _fonte_dados

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = 'senha'
uf = ''
homologacao = True
CPFCNPJ = ''
chave = ''
protocolo = ''


cancelar = EventoCancelarNota(
    cnpj=CPFCNPJ,  # cnpj do emissor
    chave=chave,  # chave de acesso da nota
    data_emissao=datetime.datetime.now(),
    uf=uf,
    protocolo=protocolo,  # número do protocolo da nota
    justificativa='Venda cancelada a pedido do cliente'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe_cancel = serializador.serializar_evento(cancelar)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe_cancel)

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.evento(modelo='nfe', evento=xml)  # modelo='nfce' ou 'nfe'

print(envio.text)
