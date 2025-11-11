import pdfplumber
import pandas as pd
import re
import os

# Carpeta donde deben colocarse los PDFs
CARPETA_PDFS = "pdfs"

def safe_extract(pattern, text):
    """Extrae un valor usando regex. Devuelve None si no encuentra."""
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else None

def extraer_altas(pdf_path, nombre_archivo):
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()

            # Separar "altas" según el patrón oficial del PDF
            bloques = t.split("Datos del Empleado")

            for bloque in bloques[1:]:
                empleado = {}
                empleado["Nombre del archivo"] = nombre_archivo

                empleado["Apellido y nombre"] = safe_extract(r"Apellido y nombre:\s*(.*)", bloque)
                empleado["CUIL"] = safe_extract(r"CUIL:\s*([0-9\-]+)", bloque)
                empleado["Fecha Inicio"] = safe_extract(r"Fecha Inicio:\s*([0-9/]+)", bloque)

                empleado["Obra Social"] = safe_extract(r"Obra Social:\s*(.*)", bloque)
                empleado["Modalidad de contrato"] = safe_extract(r"Modalidad de contrato:\s*(.*)", bloque)
                empleado["Situación de Revista"] = safe_extract(r"Situación de Revista:\s*(.*)", bloque)

                empleado["Convenio colectivo"] = safe_extract(r"Convenio colectivo:\s*(.*)", bloque)
                empleado["Categoria"] = safe_extract(r"Categoria:\s*(.*)", bloque)
                empleado["Puesto"] = safe_extract(r"Puesto:\s*(.*)", bloque)

                # Retribución pactada
                sueldo = safe_extract(r"Retrib\. pactada:\s*\$?([\d\.,]+)", bloque)
                if sueldo:
                    try:
                        empleado["Retribución pactada"] = float(sueldo.replace(".", "").replace(",", "."))
                    except:
                        empleado["Retribución pactada"] = None
                else:
                    empleado["Retribución pactada"] = None

                empleado["Mod. Liq."] = safe_extract(r"Mod\. Liq\.\:\s*(.*)", bloque)
                empleado["Domicilio de explotación"] = safe_extract(r"Domicilio de explotación:\s*(.*)", bloque)
                empleado["Actividad económica"] = safe_extract(r"Actividad económica:\s*(.*)", bloque)

                empleado["Fecha/hora envío"] = safe_extract(r"Fecha - hora de envío:\s*(.*)", bloque)

                # Guardar solo si contiene datos válidos
                if empleado["CUIL"] or empleado["Apellido y nombre"]:
                    data.append(empleado)

    return data


def main():
    todos = []

    # Leer cada PDF dentro de la carpeta /pdfs
    for archivo in os.listdir(CARPETA_PDFS):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(CARPETA_PDFS, archivo)
            nombre = os.path.splitext(archivo)[0]

            print(f"Procesando: {archivo} ...")
            datos = extraer_altas(ruta_pdf, nombre)
            todos.extend(datos)

    if not todos:
        print("⚠️ No se encontraron datos válidos en los PDFs.")
        df = pd.DataFrame({"Mensaje": ["No se detectaron altas en los PDFs"]})
    else:
        df = pd.DataFrame(todos)

    # Exportar Excel
    ruta_excel = "Altas_Tempranas_ARCA.xlsx"
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        for archivo in df["Nombre del archivo"].unique():
            hoja = archivo[:31]  # límite Excel
            df[df["Nombre del archivo"] == archivo].to_excel(writer, sheet_name=hoja, index=False)

    print("\n✅ Listo! Se generó el archivo:")
    print("   →", ruta_excel)


if __name__ == "__main__":
    main()
