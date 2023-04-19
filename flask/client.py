from requests import get, post, put, delete, patch
from sys import argv, stderr

def main():
    if len(argv) <= 2:
        print(f"USO: {argv[0]} <URL> <conta> <funcao>", file=stderr)
        exit(1)

    url = argv[1]
    conta = argv[2]
    funcao = None
    if len(argv) > 3:
        funcao = argv[3]

    if not funcao:
        r = get(f'{url}/contas/{conta}').json()
        print("Resposta:", r)
    elif funcao == 'deposito' or funcao == 'saque':
        r = patch(f'{url}/contas/{conta}/{funcao}').json()
        print("Resposta:", r)
    else:
        print(f"USO: {argv[0]} <URL> <conta> <funcao>", file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
