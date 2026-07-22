# Proyecto PayPhone en Vercel

## Descripción

Este proyecto implementa una aplicación web desarrollada con Python y Flask que integra la Cajita de Pagos de PayPhone.

La aplicación permite mostrar un catálogo de productos, iniciar un proceso de pago y procesar la respuesta enviada por PayPhone.

El proyecto fue adaptado para ejecutarse en Vercel mediante un modelo serverless y utiliza GitHub Actions para aplicar integración y despliegue continuo.

## Objetivo académico

Implementar un repositorio de código fuente conectado a un pipeline CI/CD que ejecute automáticamente las etapas de:

1. Build
2. Test
3. Deploy

El pipeline se activa cuando se realizan cambios en el repositorio de GitHub.

## Tecnologías utilizadas

- Python
- Flask
- Requests
- Pytest
- HTML
- CSS
- JavaScript
- Git
- GitHub
- GitHub Actions
- Vercel
- PayPhone

## Estructura del proyecto

```text
payphone-vervel/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── api/
│   ├── __init__.py
│   └── index.py
├── pages/
│   ├── index.html
│   └── response.html
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt