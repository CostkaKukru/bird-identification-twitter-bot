import pytest
from unittest.mock import patch
from upload_images_and_tags import upload_images_and_tags

@pytest.fixture
def mock_upload_images_and_tags():
    with patch('upload_images_and_tags.CustomVisionTrainingClient') as mock_trainer, \
         patch('upload_images_and_tags.CustomVisionPredictionClient') as mock_predictor:
        yield mock_trainer, mock_predictor

def test_upload_images_and_tags(mock_upload_images_and_tags):
    mock_trainer, mock_predictor = mock_upload_images_and_tags

    # Mock project and tag creation
    mock_project = mock_trainer.return_value.get_project.return_value
    mock_tag = mock_trainer.return_value.create_tag.return_value

    # Mock image upload
    mock_trainer.return_value.create_images_from_data.return_value = "Upload successful"

    # Call the function
    upload_images_and_tags()

    # Assert that the necessary methods were called
    mock_trainer.assert_called_once_with('azure_endpoint', 'azure_training_key')
    mock_predictor.assert_called_once_with('azure_endpoint', 'azure_prediction_key')
    mock_trainer.return_value.get_project.assert_called_once_with('25e0bd4e-3712-4d8f-a343-ce01c0b65e29')
    mock_trainer.return_value.create_tag.assert_called_once_with(mock_project.id, 'bird_name')
    mock_trainer.return_value.create_images_from_data.assert_called_once_with(mock_project.id, 'image_data', tag_ids=[mock_tag.id])