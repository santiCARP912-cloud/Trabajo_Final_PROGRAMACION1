
import csv




def _read_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            headers = reader.fieldnames or []
            return headers, rows

    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo '{path}' no existe o no se puede encontrar.")

    except PermissionError:
        raise PermissionError(f"No tenés permisos para leer el archivo '{path}'.")

    except csv.Error as e:
        raise ValueError(f"Error leyendo el CSV '{path}': {e}")

    except Exception as e:
        raise RuntimeError(f"Error inesperado leyendo '{path}': {e}")




def write_csv(path, headers, rows):
    try:
        if not headers:
            raise ValueError("No se pueden escribir CSV sin encabezados.")

        if rows is None:
            raise ValueError("Las filas no pueden ser None.")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for r in rows:
                if not isinstance(r, dict):
                    raise ValueError(f"Fila inválida: se esperaba diccionario")
                writer.writerow(r)

    except PermissionError:
        raise PermissionError(f"No tenés permisos para escribir en el archivo de salida")

    except FileNotFoundError:
        raise FileNotFoundError(f"Ruta inválida: no se pudo crear/escribir en el archivo de salida")

    except OSError as e:
        raise OSError(f"Error del sistema al escribir en el archivo de salida: {e}")

    except Exception as e:
        raise RuntimeError(f"Error inesperado en write_csv(): {e}")



