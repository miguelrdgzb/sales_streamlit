# SuperStore EDA

Análisis Exploratorio de Datos (EDA) usando Streamlit.

## Estructura del Proyecto

```plaintext
sales_streamlit/
│
├── resources/
│   └── SampleSuperStore.xls
│   └── img1.jpg
│   └── img2.jpg
│   └── img3.jpg
│   └── img4.jpg
│   └── img5.jpg
│   └── img6.jpg
└── src/
    ├── __init__.py
    ├── data_loader.py
    ├── filters.py
    ├── visualizations.py
    └── main.py

+ resources/: Contiene los archivos de datos y las capturas de pantalla.
+ src/: Contiene el código fuente del proyecto.
+ __init__.py: Archivo que marca el directorio como un paquete.
+ data_loader.py: Carga y prepara los datos.
+ filters.py: Aplica los filtros a los datos.
+ visualizations.py: Genera visualizaciones a partir de los datos.
+ main.py: Archivo principal para ejecutar la aplicación Streamlit.

## Requisitos del Sistema
+ Python 3.8 o superior
+ Librerías especificadas en requirements.txt

## Instalación

+ Clona el repositorio.
    ```git clone https://github.com/miguelrdgzb/sales_streamlit.git

+ Navega al directorio del proyecto
    ```cd sales_streamlit

+ Crea un entorno virtual
    ```python -m venv env 
    ``` env\Scripts\activate

+ Instala las dependencias
    ```pip install -r requirements.txt


## Ejecución de la aplicación

    Desde el directorio raíz del proyecto ejecuta:
    ```streamlit run src/main.py


## Muestra

![Imagen 1](resources/img1.png)
![Imagen 2](resources/img2.png)
![Imagen 3](resources/img3.png)
![Imagen 4](resources/img4.png)
![Imagen 5](resources/img5.png)
![Imagen 6](resources/img6.png)








