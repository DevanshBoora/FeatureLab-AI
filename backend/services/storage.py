from supabase import create_client, Client
from core.config import settings
from domain.exceptions import StorageException

class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket_name = "featurelab-artifacts"
        
        # Ensure bucket exists (simplified for local/demo, usually managed in Supabase dashboard)
        try:
            buckets = self.supabase.storage.list_buckets()
            if not any(b.name == self.bucket_name for b in buckets):
                self.supabase.storage.create_bucket(self.bucket_name, {"public": False})
        except Exception as e:
            # We ignore bucket creation errors as it might be permission denied with Anon Key
            # We expect the bucket to be pre-created by the user in Supabase dashboard
            pass

    def upload_file(self, file_path: str, file_bytes: bytes) -> str:
        try:
            res = self.supabase.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_bytes,
                file_options={"content-type": "application/octet-stream", "upsert": "true"}
            )
            # The returned path
            return file_path
        except Exception as e:
            raise StorageException(f"Failed to upload file to storage: {str(e)}")

    def download_file(self, file_path: str) -> bytes:
        try:
            res = self.supabase.storage.from_(self.bucket_name).download(file_path)
            return res
        except Exception as e:
            raise StorageException(f"Failed to download file from storage: {str(e)}")
