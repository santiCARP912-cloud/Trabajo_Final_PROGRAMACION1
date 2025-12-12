import argparse
import os
import json
from Secundario import _read_csv,write_csv

# Para ejecutar el programa usar: cd src/join python principal.py

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-a", type=str, default="ArchivoA.csv")
    parser.add_argument("--input-b", type=str, default="ArchivoB.csv")
    parser.add_argument("--output",  type=str, default="join_salida.csv")
    args = parser.parse_args()

    archivo_config = os.path.join(os.path.dirname(__file__), "config.json")

    try:
        with open(archivo_config, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

            args.input_a = config.get("entrada_a", args.input_a)
            args.input_b = config.get("entrada_b", args.input_b)
            args.output  = config.get("salida",    args.output)

    except FileNotFoundError:
        pass

    except json.JSONDecodeError:
        pass

    return args




def pre_join_por_comun(encabezados_a, filas_a, encabezados_b, filas_b, identico):
    if not identico:
        raise ValueError("No hay columnas en común para realizar el join.")

    final = []
    b = {}

    for FB in filas_b:
        key = tuple(FB.get(c, "") for c in identico)
        if key not in b:
            b[key] = []
        b[key].append(FB)

    for FA in filas_a:
        key = tuple(FA.get(c, "") for c in identico)

        if key in b:
            for FB in b[key]:
                combinado = {}

                for X in encabezados_a:
                    combinado[X] = FA.get(X, "")

                for X in encabezados_b:
                    if X not in identico:
                        combinado[X] = FB.get(X, "")

                final.append(combinado)

    return final

def join(input_a_path, input_b_path):
    try:
        encabezados_a, filas_a = _read_csv(input_a_path)
        encabezados_b, filas_b = _read_csv(input_b_path)

        if not encabezados_a:
            raise ValueError(f"El archivo a no tiene encabezados.")

        if not encabezados_b:
            raise ValueError(f"El archivo b no tiene encabezados.")

        
        identico = [c for c in encabezados_a if c in encabezados_b]

        if not identico:
            raise ValueError("No existen columnas en común para realizar el join.")

        out_headers = list(encabezados_a) + [c for c in encabezados_b if c not in identico]

        out_rows = pre_join_por_comun(encabezados_a, filas_a, encabezados_b, filas_b, identico)

        return out_headers, out_rows

    except FileNotFoundError as e:
        raise FileNotFoundError(f"No se pudo abrir alguno de los archivos para el join: {e}")

    except PermissionError as e:
        raise PermissionError(f"No tenés permisos para leer alguno de los archivos: {e}")

    except ValueError as e:
        raise ValueError(f"Error en el join: {e}")

    except Exception as e:
        raise RuntimeError(f"Error inesperado en join(): {e}")




if __name__ == "__main__":
    args = parse()
    headers, rows = join(args.input_a, args.input_b)
    write_csv(args.output, headers, rows)
    print(f"Join completo. Archivo de Salida: {args.output}")