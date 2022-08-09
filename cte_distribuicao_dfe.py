import urllib3
from lxml import etree

from pynfe.processamento.comunicacao import ComunicacaoCTe
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_CTE


urllib3.disable_warnings()

certificado = 'path_cert.pfx'
senha = ''
uf = ''
homologacao = True
CPFCNPJ = ''
NSU = 0
CHAVE = ''

con = ComunicacaoCTe(uf, certificado, senha, homologacao)
ultNSU = 0
maxNSU = 0
cStat = 0

while True:
    xml = con.consulta_distribuicao(cnpj=CPFCNPJ, chave=CHAVE, nsu=NSU)
    NSU = str(NSU).zfill(15)
    print(f'Nova consulta a partir do NSU: {NSU}')

    with open(f'./consulta_distrib_cte_gzip-{NSU}.xml', 'w+') as f:
        f.write(xml.text)

    resposta = etree.fromstring(xml.text.encode('utf-8'))
    ns = {'ns': NAMESPACE_CTE}

    contador_resposta = len(
        resposta.xpath(
            '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip',
            namespaces=ns))
    print(f'Quantidade de NSUs na consulta atual: {contador_resposta}')

    cStat = resposta.xpath(
        '//ns:retDistDFeInt/ns:cStat',
        namespaces=ns)[0].text
    print(f'cStat: {cStat}')

    xMotivo = resposta.xpath(
        '//ns:retDistDFeInt/ns:xMotivo',
        namespaces=ns)[0].text
    print(f'xMotivo: {xMotivo}')

    maxNSU = resposta.xpath(
        '//ns:retDistDFeInt/ns:maxNSU',
        namespaces=ns)[0].text
    print(f'maxNSU: {maxNSU}')

    # 137=nao tem mais arquivos e 138=existem mais arquivos para baixar
    if (cStat == '138'):
        for contador_xml in range(contador_resposta):
            tipo_schema = resposta.xpath(
                '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@schema',
                namespaces=ns)[contador_xml]
            numero_nsu = resposta.xpath(
                '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@NSU',
                namespaces=ns)[contador_xml]

            if (tipo_schema == 'procCTe_v3.00.xsd'):
                zip_resposta = resposta.xpath(
                    '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip',
                    namespaces=ns)[contador_xml].text
                resposta_descompactado = DescompactaGzip.descompacta(
                    zip_resposta)
                texto_descompactado = etree.tostring(
                    resposta_descompactado).decode('utf-8')

                with open(f'./consulta_distrib-nsu-{NSU}-contador-{contador_xml}.xml', 'w+', encoding='UTF-8') as f:
                    f.write(texto_descompactado)

        NSU = resposta.xpath(
            '//ns:retDistDFeInt/ns:ultNSU',
            namespaces=ns)[0].text
        print(f'NSU: {NSU}')

    elif (cStat == '137'):
        print('Não há documentos a pesquisar')
        break
    else:
        print('Falha')
        break
