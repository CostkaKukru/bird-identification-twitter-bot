from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, glob
from keys import azure_keys

def upload_images_and_tags():
	"""
	Uploads images and tags to a Custom Vision project.

	This function authenticates the client using the provided Azure keys,
	creates or updates a project, and uploads images from a dataset directory
	with corresponding tags.

	Args:
		None

	Returns:
		None
	"""
	# Replace with valid values
	ENDPOINT = azure_keys["endpoint"]
	training_key = azure_keys["training_key"]
	prediction_key = azure_keys["prediction_key"]
	prediction_resource_id = azure_keys["prediction_resource_id"]

	# Authenticate client
	credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
	trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
	prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
	predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

	# Create or update a project
	print("Creating project...")
	project_name = "JakiToPtak"
	project = trainer.get_project('25e0bd4e-3712-4d8f-a343-ce01c0b65e29')

	# Upload and tag images
	dataset_dirname = "bird images"

	dirfiles = os.listdir(dataset_dirname)
	fullpaths = map(lambda name: os.path.join(dataset_dirname, name), dirfiles)

	for file in fullpaths:
		bird_name = file.split("\\")[1]

		# Create tag
		bird_name_tag = trainer.create_tag(project.id, bird_name)

		print(f"Adding images for {bird_name} ...")
		time.sleep(1) # Wait for tag to be created to avoid too many requests


		for i, filename in enumerate(glob.glob('.\\bird images\\' + bird_name + '\\*.jpg')):
			with open(filename, "rb") as image_contents:
				image_data = image_contents.read()
				tag_ids = []
				tag_ids.append(bird_name)

				upload_result = trainer.create_images_from_data(project.id, image_data, tag_ids=[bird_name_tag.id])
				print(upload_result)

				time.sleep(1)

upload_images_and_tags()