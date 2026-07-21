import pytest

from api.index import app


@pytest.fixture()
def client():
    """
    Crea un cliente de prueba de Flask.

    No abre un navegador ni inicia un servidor real.
    Permite enviar solicitudes internas a las rutas.
    """
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_index_responde(client):
    """La página principal debe estar disponible."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"NODE" in response.data


def test_response_responde(client):
    """La página de respuesta debe estar disponible."""
    response = client.get("/response")

    assert response.status_code == 200


def test_confirm_rechaza_datos_incompletos(client):
    """
    /api/confirm debe rechazar solicitudes que no contengan
    id y clientTxId.
    """
    response = client.post("/api/confirm", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Faltan 'id' o 'clientTxId'"