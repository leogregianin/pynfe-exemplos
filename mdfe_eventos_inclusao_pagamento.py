import datetime
from decimal import Decimal
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoMDFe
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoInclusaoPagamento
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

# evento de pagamento DF-e
pagamento_dfe = EventoInclusaoPagamento(
    cnpj=CPFCNPJ,  # cpf/cnpj do emissor
    chave=chave,  # chave de acesso do MDFe
    data_emissao=datetime.datetime.now(),
    uf=uf,
    protocolo='',
    qtd_viagens='1',
    nro_viagens='1',
    nome_contratante='Teste',
    cpfcnpj_contratante='',
    tpComp='01',
    vComp=Decimal('100.00'),
    vContrato=Decimal('100.00'),
    indPag='1',
    nParcela='1',
    dVenc=datetime.datetime.now(),
    vParcela=Decimal('100.00'),
    CNPJIPEF='',
    codBanco='001',
    codAgencia='00214'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
mdfe_pagamento_dfe = serializador.serializar_evento_mdfe(pagamento_dfe)

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(mdfe_pagamento_dfe)

# transmissão
envio = mdfe.evento(evento=xml)
print(envio.text)
