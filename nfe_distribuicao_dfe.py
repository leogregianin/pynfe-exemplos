import urllib3
from lxml import etree

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE

urllib3.disable_warnings()


certificado = 'path_cert.pfx'
senha = ''
uf = 'MT'
homologacao = True
CPFCNPJ = ''
NSU = 0
CHAVE = ''


con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
ultNSU = 0
maxNSU = 0
cStat = 0

while True:
    xml = con.consulta_distribuicao(cnpj=CPFCNPJ, chave=CHAVE, nsu=NSU)
    NSU = str(NSU).zfill(15)
    print(f'Nova consulta a partir do NSU: {NSU}')

    resposta = etree.fromstring(xml.text.encode('utf-8'))
    ns = {'ns': NAMESPACE_NFE}

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

            # nfe = 'procNFe_v4.00.xsd'
            # evento = 'procEventoNFe_v1.00.xsd'
            # resumo = 'resNFe_v1.01.xsd'
            if (tipo_schema == 'procNFe_v4.00.xsd'):
                zip_resposta = resposta.xpath(
                    '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip',
                    namespaces=ns)[contador_xml].text
                resposta_descompactado = DescompactaGzip.descompacta(
                    zip_resposta)
                texto_descompactado = etree.tostring(
                    resposta_descompactado).decode('utf-8')

                with open(f'./consulta_distrib-nsu-{NSU}-contador-{contador_xml}.xml', 'w+', encoding='UTF-8') as f:
                    f.write(texto_descompactado)

            # baixar o resumo e realizar a manifestacao do destinatario
            elif (tipo_schema == 'resNFe_v1.01.xsd'):
                zip_resposta = resposta.xpath(
                    '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip',
                    namespaces=ns)[contador_xml].text

                # XML completo do resumo
                resposta_descompactado = DescompactaGzip.descompacta(
                    zip_resposta)

                # Ler chave de acesso do resumo
                chave_acesso_nfe = resposta_descompactado.xpath(
                    '//ns:resNFe/ns:chNFe', namespaces=ns)[0].text

                # Gerar ciência da operação
                # https://github.com/TadaSoftware/PyNFe/wiki/Manifesta%C3%A7%C3%A3o-Destinat%C3%A1rio

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
