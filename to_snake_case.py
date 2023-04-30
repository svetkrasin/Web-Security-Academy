import sys

if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <string-to-converte>")
    print('-'.join(sys.argv[1:]))