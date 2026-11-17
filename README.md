# Presentación de Agroindustrias del Tolima S.A.S.

Proyecto web estático para GitHub Pages: **10 diapositivas**, dashboard de pronósticos y KPI, fortalezas/debilidades de Excel vs. IA, diferencias estadísticas, flujo híbrido y reflexión.

## Subir a GitHub (interfaz en español)

1. Descarga y **extrae** `PROYECTO_LISTO_PARA_GITHUB.zip`. No subas el ZIP sin extraer.
2. En tu repositorio `Lalis201/pronosticos-agroindustrias-tolima`, pulsa **Agregar archivo → Cargar archivos**.
3. Selecciona **todos los archivos extraídos** y confirma con **Confirmar cambios**. Si GitHub pregunta por reemplazar archivos existentes, confirma la actualización; no crees otro repositorio.
4. En **Configuración → Páginas**, busca **Compilación e implementación** y elige **Implementar desde una rama**.
5. Selecciona la rama que aparezca en el repositorio: en tus capturas se llama `principal`; carpeta `/(root)` o `/(raíz)`. Pulsa **Guardar**.
6. Cuando termine el despliegue, abre https://lalis201.github.io/pronosticos-agroindustrias-tolima/ . Si no se publica, revisa **Acciones** y **Páginas** para identificar el error.

## Notas académicas

- Fuente: `1 taller(6).xlsx`; 36 meses, enero de 2024 a diciembre de 2026, valores en miles de COP.
- `validar_modelos.py` permite repetir los cálculos con numpy y statsmodels.
- Los errores son de validación retrospectiva a un paso; **no prueban** cuál método es óptimo a seis meses.
- Los escenarios porcentuales son análisis de sensibilidad, no intervalos de confianza.
- Costos y gastos futuros son estimaciones, no presupuestos aprobados.
