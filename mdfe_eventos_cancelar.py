import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoMDFe
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoCancelarNota
from pynfe.entidades.fonte_dados import _fonte_dados

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = ''
uf = ''
homologacao = True
CPFCNPJ = ''
chave = ''
protocolo = ''

mdfe = ComunicacaoMDFe(uf, certificado, senha, homologacao)

# evento de cancelamento
cancelar = EventoCancelarNota(
    cnpj=CPFCNPJ,  # cpf/cnpj do emissor
    chave=chave,  # chave de acesso do MDFe
    data_emissao=datetime.datetime.now(),
    uf=uf,
    protocolo=protocolo,  # número do protocolo do envio do MDFe
    justificativa='Erro na inclusao das informacoes do manifesto'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
mdfe_cancelamento = serializador.serializar_evento(cancelar)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(mdfe_cancelamento)

# transmissão
envio = mdfe.evento(evento=xml)
print(envio.text)
