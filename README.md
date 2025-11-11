# ARCA Altas Tempranas Parser

Este repositorio contiene un script que permite procesar automáticamente archivos PDF de Altas Tempranas de ARCA y generar un archivo Excel con todos los datos estructurados.

El script:
✅ Extrae la información de cada alta individual.  
✅ Procesa tantos PDFs como subas.  
✅ Limpia y estructura los datos.  
✅ Genera un archivo Excel final con una hoja por empresa.

Ideal para estudios contables, recursos humanos o automatización documental.

---

## 📌 Funcionalidades principales
- Lectura de PDFs mediante `pdfplumber`
- Extracción de campos clave:
  - CUIL del empleado  
  - Nombre completo  
  - Fecha de inicio de la relación laboral  
  - Obra social  
  - Modalidad de contratación  
  - Situación de revista  
  - Convenio colectivo  
  - Categoría / Puesto  
  - Remuneración pactada  
  - Modalidad de liquidación  
  - Domicilio  
  - Actividad económica  
  - Fecha/hora de carga  
  - Nombre y CUIT del empleador  
- Exportación a Excel con una hoja por empresa
- Compatible 100% con Google Colab

---

## ▶️ Ejecución
1. Abrir el script en Google Colab  
2. Ejecutar las celdas según el orden  
3. Subir los PDFs cuando te los pida  
4. Descargar el Excel generado automáticamente

---

## 📁 Archivo generado
`Resumen_Altas_Tempranas.xlsx`, con una hoja por empresa.

---

## ⚠️ Limitaciones
- El PDF debe tener estructura estándar de ARCA  
- Si los textos están cortados, puede omitir campos  
- La detección se basa en búsqueda textual simple

---

## ✅ Licencia
Uso libre. Podés modificarlo, reutilizarlo o adaptarlo.

---

# Instrucciones para ejecutar la versión Google Colab

1) Abrir Google Colab:
   https://colab.research.google.com

2) Crear un nuevo notebook y pegar el script completo.

3) Ejecutar la primera celda:
   - Instala pdfplumber, openpyxl y pandas.

4) Ejecutar la celda donde aparece:
   uploaded = files.upload()
   - Subir todos los PDF de Altas Tempranas generados por ARCA.

5) Ejecutar las siguientes celdas normalmente.
   El script extraerá todos los campos automáticamente.

6) Al final se generará:
   Resumen_Altas_Tempranas.xlsx

7) Google Colab ofrecerá la descarga automática.


