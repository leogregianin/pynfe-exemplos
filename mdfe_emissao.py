import datetime
from decimal import Decimal

from lxml import etree
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoMDFe
from pynfe.processamento.serializacao import (
    SerializacaoMDFe,
    SerializacaoQrcodeMDFe
)
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.manifesto import (
    Manifesto,
    ManifestoEmitente,
    ManifestoTotais,
    ManifestoMunicipioCarrega,
    ManifestoPercurso,
    ManifestoAverbacao,
    ManifestoDocumentosNFe,
    ManifestoRodoviario,
    ManifestoVeiculoTracao,
    ManifestoVeiculoReboque,
    ManifestoCondutor,
    ManifestoCIOT,
    ManifestoPedagio,
    ManifestoContratante
)
from pynfe.entidades.fonte_dados import _fonte_dados

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = ''
uf = ''
homologacao = True

CPFCNPJ = ''
IE = ''
numero_mdfe = 1
serie = '001'
uf = ''
homologacao = True
ind_sinc = 0  # forma de envio: 0=assincrono; 1=sincrono


# Emitente
emitente = ManifestoEmitente(
    cpfcnpj=CPFCNPJ,  # cnpj apenas números
    inscricao_estadual=IE,  # numero de IE da empresa
    razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
    nome_fantasia='Nome Fantasia da Empresa',
    endereco_logradouro='RUA UM',
    endereco_numero='111',
    endereco_complemento=None,
    endereco_bairro='CENTRO',
    endereco_municipio='CUIABA',
    endereco_cep='78118000',
    endereco_uf='MT',
    endereco_telefone='65999662821',
    endereco_email='teste@gmail.com'
)

# Totais
totais = ManifestoTotais(
    qCTe=0,
    qNFe=2,
    vCarga=1000,
    cUnid='KG',
    qCarga=5000
)

# Municípios de carregamento
carregamento_1 = ManifestoMunicipioCarrega(
    cMunCarrega='5105101',
    xMunCarrega='JUARA'
)
carregamento_2 = ManifestoMunicipioCarrega(
    cMunCarrega='5107925',
    xMunCarrega='SORRISO'
)

# UFs percurso
percurso_1 = ManifestoPercurso(UFPer='MS')
percurso_2 = ManifestoPercurso(UFPer='GO')


# modal Rodo
condutor_1 = ManifestoCondutor(
    nome_motorista='JOAO DA SILVA',
    cpf_motorista='12345678912'
)
condutor_2 = ManifestoCondutor(
    nome_motorista='JOSE DA SILVA',
    cpf_motorista='12345678911'
)

veiculo_tracao = ManifestoVeiculoTracao(
    cInt='001',
    placa='ABC1234',
    RENAVAM='123456789',
    tara='5000',
    capKG='4500',
    capM3='400',
    proprietario=None,
    condutor=[condutor_1, condutor_2],
    tpRod='01',
    tpCar='02',
    UF='MT'
)

veiculo_reboque_1 = ManifestoVeiculoReboque(
    cInt='001',
    placa='XYZ4567',
    RENAVAM='123456789',
    tara='4000',
    capKG='3000',
    capM3='300',
    proprietario=None,
    tpCar='02',
    UF='MT'
)

veiculo_reboque_2 = ManifestoVeiculoReboque(
    cInt='002',
    placa='XYQ4567',
    RENAVAM='123456781',
    tara='4000',
    capKG='3000',
    capM3='300',
    proprietario=None,
    tpCar='02',
    UF='MT'
)

ciot_1 = ManifestoCIOT(
    numero_ciot='123456789012',
    cpfcnpj=''
)

pedagio_1 = ManifestoPedagio(
    cnpj_fornecedor='04352277000134',
    cpfcnpj_pagador='',
    numero_compra='789',
    valor_pedagio=Decimal('2.64')
)

contratante_1 = ManifestoContratante(
    nome='JOAO DA SILVA',
    cpfcnpj='12345678912'
)
contratante_2 = ManifestoContratante(
    nome='JOSE DA SILVA',
    cpfcnpj='12345678911'
)

modal_rodoviario = ManifestoRodoviario(
    rntrc='12345678',
    ciot=[ciot_1],
    pedagio=[pedagio_1],
    contratante=[contratante_1, contratante_2],
    pagamento=None,
    veiculo_tracao=veiculo_tracao,
    veiculo_reboque=[veiculo_reboque_1, veiculo_reboque_2]
)

# Manifesto
manifesto = Manifesto(
    uf=uf.upper(),
    tipo_emitente=2,  # 1=Transportadora; 2=Carga própria; 3=CTe Globalizado
    tipo_transportador=0,  # 0=nenhum; 1=etc; 2=tac; 3=ctc
    modelo=58,
    serie=serie,
    numero_mdfe=numero_mdfe,
    modal=1,
    data_emissao=datetime.datetime.now(),
    forma_emissao='1',  # 1=Emissão normal (não em contingência);
    processo_emissao='0',  # 0=Emissão de NF-e com aplicativo do contribuinte;
    UFIni='MT',
    UFFim='SP',
    infMunCarrega=[carregamento_1, carregamento_2],
    infPercurso=[percurso_1, percurso_2],
    dhIniViagem=datetime.datetime.now(),
    emitente=emitente,
    modal_rodoviario=modal_rodoviario,
    # documentos=None,
    totais=totais,
    informacoes_complementares_interesse_contribuinte='Mensagem complementar'
)

# Documentos vinculados
nfe_1 = ManifestoDocumentosNFe(chave_acesso_nfe='chave_de_acesso_nfe_1')
nfe_2 = ManifestoDocumentosNFe(chave_acesso_nfe='chave_de_acesso_nfe_2')
nfe_3 = ManifestoDocumentosNFe(chave_acesso_nfe='chave_de_acesso_nfe_3')
nfe_4 = ManifestoDocumentosNFe(chave_acesso_nfe='chave_de_acesso_nfe_4')

manifesto.adicionar_documentos(
    cMunDescarga='3550308',
    xMunDescarga='Sao Paulo',
    documentos_nfe=[nfe_1, nfe_2],
    documentos_cte=[]
)
manifesto.adicionar_documentos(
    cMunDescarga='3530607',
    xMunDescarga='Mogi das Cruzes',
    documentos_nfe=[nfe_3, nfe_4],
    documentos_cte=[]
)


# Informações do Seguro
averbacao_1 = ManifestoAverbacao(numero='00000000000000000000000')
averbacao_2 = ManifestoAverbacao(numero='11111111111111111111111')

manifesto.adicionar_seguradora(
    responsavel_seguro='1',
    cnpj_responsavel='',
    nome_seguradora='SEGURADORA SA',
    cnpj_seguradora='',
    numero_apolice='00000',
    averbacoes=[averbacao_1, averbacao_2]
)

# Produto Predominante
manifesto.adicionar_produto(
    tipo_carga='01',
    nome_produto='Descricao do Produto',
    cean='78967142344650',
    ncm='01012100'
)

# Lacres
manifesto.adicionar_lacres(nLacre='123')
manifesto.adicionar_lacres(nLacre='456')
manifesto.adicionar_lacres(nLacre='789')

# Responsável técnico
manifesto.adicionar_responsavel_tecnico(
    cnpj='',
    contato='LA Software',
    email='l@global.com',
    fone='11981447111'
)


# Serialização
serializador = SerializacaoMDFe(_fonte_dados, homologacao=homologacao)
mdfe = serializador.exportar()

# Assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(mdfe)

# Gera e adiciona o qrcode no xml
xml_com_qrcode = SerializacaoQrcodeMDFe().gerar_qrcode(xml)

# envio
con = ComunicacaoMDFe(uf, certificado, senha, homologacao)
envio = con.autorizacao(manifesto=xml, ind_sinc=ind_sinc)

# em caso de sucesso o retorno será o xml autorizado
# Ps: no modo sincrono, o retorno será o xml completo,
# ou seja, <nfeProc> = <NFe> + <protNFe>
# no modo async é preciso montar o nfeProc, juntando o retorno com a NFe
if envio[0] == 0:
    print('Sucesso!')
    xml = etree.tostring(
        envio[1],
        encoding="unicode"
    ).replace('\n', '').replace('ns0:', '')
    # em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
else:
    print('Erro:')
    print(envio[1].text)
    # print('Nota:')
    xml = etree.tostring(envio[2], encoding="unicode")

# filename = f'emissao_mdfe-{numero_mdfe}.xml'
# with open(filename, 'w+', encoding='UTF-8') as f:
#     f.write(xml)
