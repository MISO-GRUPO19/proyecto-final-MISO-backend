from manufacturers_management.src.models.model import Model

def test_base_model():
    model = Model()
    assert model is not None