from pynfe.processamento.comunicacao import ComunicacaoMDFe
import urllib3

urllib3.disable_warnings()


certificado = "path_cert.pfx"
senha = ''
uf = ''
homologacao = True
CPFCNPJ = ''
chave = ''
protocolo = ''

mdfe = ComunicacaoMDFe(uf, certificado, senha, homologacao)
mdfe_recibo = mdfe.consulta_recibo('cnpj')
print(mdfe_recibo.text)
