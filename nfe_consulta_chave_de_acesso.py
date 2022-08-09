import urllib3
from lxml import etree

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.flags import NAMESPACE_NFE


urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = 'senha'
uf = ''
homologacao = True
CPFCNPJ = ''
IE = ''
chave = ''
protocolo = ''


con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.consulta_nota('nfe', chave)  # nfe ou nfce
print(envio.text.encode('utf-8'))

ns = {'ns': NAMESPACE_NFE}
prot = etree.fromstring(envio.text.encode('utf-8'))
status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
if status == '100':
    prot_nfe = prot[0][0].xpath(
        'ns:retConsSitNFe/ns:protNFe',
        namespaces=ns)[0]
    xml = etree.tostring(prot_nfe, encoding='unicode')
    print(xml)
