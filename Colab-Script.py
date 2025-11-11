# ⬇️ Instalar bibliotecas necesarias
!pip install pdfplumber openpyxl pandas

import pdfplumber
import pandas as pd
import os

# ⬇️ Subir archivos PDF
from google.colab import files
uploaded = files.upload()

# ⬇️ Función para extraer los datos de un PDF de ARCA
def extraer_datos(pdf_path, nombre_archivo):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            bloques = text.split("CUIL del trabajador:")
            for bloque in bloques[1:]:
                try:
                    trabajador = {}
                    trabajador["Nombre del archivo"] = nombre_archivo

                    trabajador["CUIL del empleado"] = bloque.split("\n")[0].strip()
                    trabajador["Apellido y nombre del empleado"] = bloque.split("Apellido y nombre del trabajador:")[1].split("\n")[0].strip()
                    trabajador["Fecha de inicio"] = bloque.split("Fecha de inicio de la relación laboral:")[1].split("\n")[0].strip()
                    trabajador["Obra social"] = bloque.split("Obra social:")[1].split("\n")[0].strip()
                    trabajador["Modalidad de contrato"] = bloque.split("Modalidad de contratación:")[1].split("\n")[0].strip()
                    trabajador["Situación de revista"] = "Activo"
                    trabajador["Convenio colectivo"] = bloque.split("Convenio colectivo:")[1].split("\n")[0].strip()
                    trabajador["Categoría / Puesto"] = bloque.split("Categoría:")[1].split("\n")[0].strip()

                    try:
                        trabajador["Retribución pactada"] = float(bloque.split("Remuneración pactada:")[1].split("\n")[0].replace(".", "").replace(",", ".").replace("$", "").strip())
                    except:
                        trabajador["Retribución pactada"] = None

                    trabajador["Modalidad de liquidación"] = bloque.split("Modalidad de liquidación:")[1].split("\n")[0].strip()
                    trabajador["Domicilio de explotación"] = bloque.split("Domicilio de explotación:")[1].split("\n")[0].strip()
                    trabajador["Actividad económica"] = bloque.split("Actividad principal:")[1].split("\n")[0].strip()
                    trabajador["Fecha/hora de alta"] = bloque.split("Fecha/hora de carga:")[1].split("\n")[0].strip() if "Fecha/hora de carga:" in bloque else None
                    trabajador["Nombre del empleador"] = bloque.split("Empleador:")[1].split("\n")[0].strip()
                    trabajador["CUIT del empleador"] = bloque.split("CUIT del empleador:")[1].split("\n")[0].strip()

                    data.append(trabajador)
                except:
                    pass
    return data


# ⬇️ Procesar todos los PDFs subidos
todos_los_datos = []
for nombre_archivo in uploaded.keys():
    datos = extraer_datos(nombre_archivo, os.path.splitext(nombre_archivo)[0])
    todos_los_datos.extend(datos)

# ⬇️ Convertir a DataFrame
df = pd.DataFrame(todos_los_datos)

# ⬇️ Generar un Excel con una hoja por empresa
ruta_excel = "Resumen_Altas_Tempranas.xlsx"
with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
    for empresa in df["Nombre del archivo"].unique():
        hoja = empresa[:31]
        df_empresa = df[df["Nombre del archivo"] == empresa].drop(columns=["Nombre del archivo"])
        df_empresa.to_excel(writer, sheet_name=hoja, index=False)

# ⬇️ Descargar archivo Excel
files.download(ruta_excel)
