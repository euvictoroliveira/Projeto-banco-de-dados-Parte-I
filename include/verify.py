import re

def validar_cpf(cpf):
    # Remove tudo que não for número (pontos e traços)
    cpf = re.sub(r'[^0-9]', '', str(cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
        
    # Elimina CPFs com todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return False
        
    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    
    resto = (soma * 10) % 11

    if resto == 10: resto = 0

    if resto != int(cpf[9]):

        return False
        
    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))

    resto = (soma * 10) % 11

    if resto == 10: resto = 0

    if resto != int(cpf[10]):
        return False
        
    return True

def validar_crm(crm):

    if not crm:
        return False
        
    # Tira espaços das pontas e deixa tudo maiúsculo
    crm = str(crm).strip().upper()
    
    # Regex: Padrão -> De 4 a 10 números + separador opcional + 2 letras do Estado
    padrao = r'^\d{4,10}[/\-\s]?[A-Z]{2}$'
    
    if re.match(padrao, crm):
        return True
        
    return False