from lxml import etree
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.flags import NAMESPACE_NFE

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = 'senha'
uf = ''
homologacao = True

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.status_servico('nfe')  # nfe ou nfce
print(xml.text)

# exemplo de leitura da resposta
ns = {'ns': NAMESPACE_NFE}
resposta = etree.fromstring(xml.content)[0][0]

status = resposta.xpath('ns:retConsStatServ/ns:cStat', namespaces=ns)[0].text
print(status)
motivo = resposta.xpath('ns:retConsStatServ/ns:xMotivo', namespaces=ns)[0].text
print(motivo)
