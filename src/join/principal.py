import argparse
import csv
import os
import json


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-a", type=str, default="ArchivoA.csv")
    parser.add_argument("--input-b", type=str, default="ArchivoB.csv")
    parser.add_argument("--output",  type=str, default="join_salida.csv")
    args = parser.parse_args()

    archivo_config = os.path.join(os.path.dirname(_file_), "config.json")

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


def _read_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            headers = reader.fieldnames or []
            return headers, rows

    except FileNotFoundError:
        raise FileNotFoundError("El archivo no existe o no se puede encontrar.")

    except PermissionError:
        raise PermissionError("No tenés permisos para leer el archivo.")

    except csv.Error as e:
        raise ValueError(f"Error leyendo el CSV: {e}")

    except Exception as e:
        raise RuntimeError(f"Error inesperado leyendo: {e}")