import urllib3

from pynfe.processamento.comunicacao import ComunicacaoCTe

urllib3.disable_warnings()


certificado = 'path_cert.pfx'
senha = ''
uf = ''
homologacao = True
CPFCNPJ = ''


con = ComunicacaoCTe(uf, certificado, senha, homologacao)
xml = con.status_servico()
print(xml.text)
