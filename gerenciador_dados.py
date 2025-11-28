import json
import os

diretorio_script = os.path.dirname(os.path.abspath(__file__))

NOME_ARQUIVO = os.path.join(diretorio_script, 'dados.json')


def criar_pessoa(id_pessoa: int, nome: str, idade:int, email:str, universidade: str) -> dict:
    contexto = {
        "@context" : "https://schema.org/",
        "@type" : "person",
    }
    dados = {
        "@id" : f"urn : pessoa : {id_pessoa}",
        "nome" : nome,
        "idade" : idade,
        "email" : email,
        "universidade" : {
            "@type" : "Organization",
            "nome" : universidade,
        }
    }

    dados_completos = {**contexto, **dados}

    return dados_completos

if __name__ == "__main__":
    lista_de_pessoas =[]
    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
            lista_de_pessoas = json.load(f)

            if not isinstance(lista_de_pessoas, list):
                lista_de_pessoas = []
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    novo_id = len(lista_de_pessoas) + 1

    novo_nome = input("digite o nome:").strip()
    novo_idade = int(input("digite a idade:").strip())
    novo_email = input("digite o email:").strip()
    nova_universidade = "UFES"
    #entrada para as variaveis

    nova_pessoa = criar_pessoa (
        id_pessoa=novo_id,
        nome=novo_nome,
        idade=novo_idade,
        email=novo_email,
        universidade=nova_universidade
        # para cada nova pessoa
    )
    
lista_de_pessoas.append(nova_pessoa)
# Salvar a lista de pessoas no arquivo JSON

try: 
    with open(NOME_ARQUIVO, 'w',encoding='utf-8') as f:
        #salva a nova lista de pessoas
        json.dump(lista_de_pessoas, f, ensure_ascii=False, indent=4)

        print(f"\n'{novo_nome}' foi add")

except IOError as e:
    print(f"error ao salvar o arquivo: {e}")