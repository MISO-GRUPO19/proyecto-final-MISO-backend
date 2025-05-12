import uuid
import threading
from ..models.video import Video, VideoStatus
from ..models.database import db_session
from flask import current_app
from google.cloud import storage
from ..pubsub.publisher import publish_message

PROCESS_RESULTS = {}

class ProcessVideo:
    def __init__(self, video_file, visit_id):
        self.video_file = video_file
        self.visit_id = visit_id

    def execute(self):
        video_id = str(uuid.uuid4())
        gcs_path = f"videos/{video_id}.mp4"
        public_url = self.upload_to_gcs(self.video_file, gcs_path)

        new_video = Video(
            fileInfo=public_url,
            name=self.video_file.filename,
            visitId=self.visit_id,
            status=VideoStatus.processing
        )

        db_session.add(new_video)
        db_session.commit()

        publish_message('videos', {'video_id': str(new_video.id)})
        
        return {"video_id": video_id, "status": "PROCESANDO"}

    def upload_to_gcs(self, file_obj, destination_blob_name, bucket_name="videos_tiendas_g19"):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        file_obj.stream.seek(0)
        blob.upload_from_file(file_obj.stream, content_type=file_obj.content_type)
        return blob.public_url
    

class GetVideoResult:
    def __init__(self, visit_id):
        self.visit_id = visit_id

    def execute(self):
        video = db_session.query(Video).filter_by(visitId=self.visit_id).first()

        if not video:
            return {"error": "Video no encontrado"}

        return {
            "video_id": video.id,
            "status": video.status.value,
            "result": video.results
        }
