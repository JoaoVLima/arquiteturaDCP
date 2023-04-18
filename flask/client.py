from requests import get, post, put, delete, patch
from sys import argv, stderr

def main():
    if len(argv) < 2:
        print(f"USO: {argv[0]} <URL> <msg>", file=stderr)
        exit(1)

    url = argv[1]
    msg = " ".join(argv[2:])
    r = patch(url + "/eco/" + msg).json()
    print("Resposta:", r['resp'])
    r = get(url + "/eco").json()
    print("Contador:", int(r['cont']))

if __name__ == '__main__':
    main()
