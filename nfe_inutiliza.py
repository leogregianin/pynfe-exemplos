import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz

urllib3.disable_warnings()


certificado = 'path_cert.pfx'
senha = ''
uf = ''
homologacao = True
CPFCNPJ = ''

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.inutilizacao(
    modelo='nfe',  # nfe ou nfce
    cnpj=CPFCNPJ,  # cnpj do emitente
    numero_inicial=1,  # Número da NF-e inicial a ser inutilizada
    numero_final=1,  # Número da NF-e final a ser inutilizada
    justificativa='Informar a justificativa',  # Informar a justificativa do pedido de inutilização (min 15 max 255)  # noqa
    ano=2020,
    serie='101')

print(envio.text)
