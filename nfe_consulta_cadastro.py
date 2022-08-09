from pynfe.processamento.cominucacao import ComunicacaoSefaz


certificado = "path_cert.pfx"
senha = 'senha'
uf = ''
homologacao = True

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_cadastro('nfe', 'cnpj')
print(xml.text)
