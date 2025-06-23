import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pymupdf
import os

def generar_nombre_unico(base_path: Path) -> Path:
  # Si base_path existe, agrega _1, _2, etc. al nombre hasta que no exista.
  print("base_path: ", base_path)
  if not base_path.exists():
    return base_path
  
  contador = 1
  while True:
    nuevo_nombre = base_path.with_stem(f"{base_path.stem}_{contador}")
    print("nuevo_nombre: ", nuevo_nombre)
    if not nuevo_nombre.exists():
      return nuevo_nombre
    contador += 1

def seleccionar_ruta(title):
  root = tk.Tk()
  root.withdraw()  # Oculta la ventana principal de Tkinter
  ruta = filedialog.askdirectory(title=title)
  if ruta:
    print(f"Ruta seleccionada: {ruta}")
  else:
    print("No se seleccionó ninguna carpeta.")
  return Path(ruta)

def generar_pdf_filtrado(pagina, path_root):
  pdf_filtrado = pymupdf.open()
  pdf_filtrado.insert_pdf(archivo_actual, from_page=pagina, to_page=pagina)

  nombre_base = Path(f"{path_root}/{palabra.strip().upper()}_{file}")
  ruta_final = generar_nombre_unico(nombre_base)

  pdf_filtrado.save(ruta_final)
  pdf_filtrado.close()

# Se selecciona pdf donde se buscara los datos ingresados
carpeta_origen = seleccionar_ruta("Seleccionar ruta a buscar")
palabras_clave = input("Ingrese las palabras clave separadas por comas sin espacios: ").strip().split(',')
carpeta_salida = seleccionar_ruta("Seleccionar carpeta de destino")
pagina_encontrada = []

print("Buscando palabras clave...")
for root, _, files in os.walk(carpeta_origen):
  for file in files:
    if file.endswith(".pdf"):
      archivo_actual = pymupdf.open(Path(root)/file)
      for pagina in archivo_actual:
        texto_pagina = pagina.get_text().lower()
        for palabra in palabras_clave:
          if palabra.strip().lower() in texto_pagina:
            generar_pdf_filtrado(pagina.number, carpeta_salida)
            break

      archivo_actual.close()
  