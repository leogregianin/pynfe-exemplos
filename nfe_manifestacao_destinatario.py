import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoManifestacaoDest
from pynfe.entidades.fonte_dados import _fonte_dados

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = ''
uf = 'AN'
homologacao = True
CPFCNPJ = ''
IE = ''
chave = ''


# Tipo de Operação:
# 1=Confirmação da Operação
# 2=Ciência da Emissão
# 3=Desconhecimento da Operação
# 4=Operação não Realizada
manif_dest = EventoManifestacaoDest(
    cnpj=CPFCNPJ,  # cnpj do destinatário
    chave=chave,  # chave de acesso da nota
    data_emissao=datetime.datetime.now(),
    uf=uf,
    operacao=2
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe_manif = serializador.serializar_evento(manif_dest)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe_manif)

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.evento(modelo='nfe', evento=xml)  # modelo='nfce' ou 'nfe'
print(envio.text)
