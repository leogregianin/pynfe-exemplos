import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoMDFe
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoInclusaoCondutor
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

# evento de inclusao de condutor
inclusao_condutor = EventoInclusaoCondutor(
    cnpj=CPFCNPJ,  # cpf/cnpj do emissor
    chave=chave,  # chave de acesso do MDFe
    data_emissao=datetime.datetime.now(),
    uf=uf,
    nome_motorista='Teste',
    cpf_motorista='123'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
mdfe_inclusao_condutor = serializador.serializar_evento_mdfe(inclusao_condutor)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(mdfe_inclusao_condutor)

# transmissão
envio = mdfe.evento(evento=xml)
print(envio.text)
