import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

import pruebas as p
import graficas as g
from ui_generador import abrir_generador

numeros = []

def set_numeros(nuevos):
    global numeros
    numeros = nuevos

def cargar_datos():
    global numeros
    archivo = filedialog.askopenfilename(filetypes=[("Excel","*.xlsx *.xls")])
    if not archivo:
        return
    df = pd.read_excel(archivo)
    numeros = df[df.columns[0]].dropna().tolist()
    messagebox.showinfo("OK", f"{len(numeros)} datos cargados")

def ejecutar():
    if not numeros:
        return

    resultado.delete("1.0", tk.END)

    if metodo.get()=="poker":
        frec = p.contar_frecuencias(numeros)
        tabla = p.generar_tabla(frec,len(numeros))

        tabla_agrupada = p.agrupar_categorias(tabla)
        chi = p.chi_cuadrado_agrupado(tabla_agrupada)
        
        gl = obtener_gl_usuario(tabla_agrupada)
        chi_critico = p.obtener_chi_critico(gl)

        resultado.insert(tk.END,"TABLA AGRUPADA\n")
        for t in tabla_agrupada:
            resultado.insert(tk.END,f"{t}\n")

        resultado.insert(tk.END,f"\nChi={chi}")

        resultado.insert(tk.END, f"\nGL = {gl}\n")
        resultado.insert(tk.END, f"Chi crítico = {chi_critico}\n")
        if chi_critico:
            if chi < chi_critico:
                resultado.insert(tk.END, "Resultado: ACEPTA H0\n")
            else:
                resultado.insert(tk.END, "Resultado: RECHAZA H0\n")
        else:
            resultado.insert(tk.END, "GL fuera de tabla (usa más valores)\n")

    elif metodo.get()=="corridas":
        binaria = p.generar_binaria(numeros)
        corr = p.obtener_corridas(binaria)
        FO = p.frecuencia_corridas(corr)

        n = len(numeros)
        max_long = max(FO.keys())
        FE = p.frecuencia_esperada_corridas(n, max_long)

        tabla = p.tabla_corridas(FO, FE)
        tabla_agrupada = p.agrupar_categorias(tabla)

        chi = p.chi_cuadrado_agrupado(tabla_agrupada)

        resultado.insert(tk.END,"TABLA AGRUPADA\n")
        for t in tabla_agrupada:
            resultado.insert(tk.END,f"{t}\n")

        resultado.insert(tk.END,f"\nChi={chi}")

    elif metodo.get()=="ks":
        D,_,_ = p.kolmogorov_smirnov(numeros)
        resultado.insert(tk.END,f"D={D}")

def graficar():
    if metodo.get()=="poker":
        frec = p.contar_frecuencias(numeros)
        g.graficar_poker(p.generar_tabla(frec,len(numeros)))

    elif metodo.get()=="corridas":
        corr = p.obtener_corridas(p.generar_binaria(numeros))
        g.graficar_corridas(p.frecuencia_corridas(corr))

    elif metodo.get()=="ks":
        g.graficar_ks(numeros)

    g.histograma(numeros)
    g.dispersion(numeros)

def obtener_gl_usuario(tabla_agrupada):
    valor = entry_gl.get().strip()

    if valor != "":
        return int(valor)
    else:
        return len(tabla_agrupada) - 1

# UI
ventana = tk.Tk()
metodo = tk.StringVar(value="poker")

tk.Radiobutton(ventana,text="Poker",variable=metodo,value="poker").pack()
tk.Radiobutton(ventana,text="Corridas",variable=metodo,value="corridas").pack()
tk.Radiobutton(ventana,text="KS",variable=metodo,value="ks").pack()

tk.Button(ventana,text="Cargar",command=cargar_datos).pack()
tk.Button(ventana, text="Generar números", command=lambda: abrir_generador(set_numeros)).pack()
tk.Button(ventana,text="Ejecutar",command=ejecutar).pack()
tk.Button(ventana,text="Graficar",command=graficar).pack()
tk.Label(ventana, text="Grados de libertad (opcional):").pack()

entry_gl = tk.Entry(ventana)
entry_gl.pack()

resultado = tk.Text(ventana)
resultado.pack()

ventana.mainloop()