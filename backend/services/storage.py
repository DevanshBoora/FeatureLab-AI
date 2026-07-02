from supabase import create_client, Client
from core.config import settings
from domain.exceptions import StorageException

class StorageService:
    def __init__(self):
        self.bucket_name = "featurelab-artifacts"
        self.supabase = None
        try:
            self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            # Ensure bucket exists (simplified for local/demo, usually managed in Supabase dashboard)
            buckets = self.supabase.storage.list_buckets()
            if not any(b.name == self.bucket_name for b in buckets):
                self.supabase.storage.create_bucket(self.bucket_name, {"public": False})
        except Exception as e:
            # Catch Invalid API Key or network errors so the app doesn't crash entirely.
            print(f"Storage init bypassed due to error: {e}")
            self.supabase = None

    def upload_file(self, file_path: str, file_bytes: bytes) -> str:
        if not self.supabase:
            print(f"Supabase client not initialized, skipping upload for {file_path}")
            return file_path
            
        try:
            res = self.supabase.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_bytes,
                file_options={"content-type": "application/octet-stream", "upsert": "true"}
            )
            return file_path
        except Exception as e:
            raise StorageException(f"Failed to upload file to storage: {str(e)}")

    def download_file(self, file_path: str) -> bytes:
        if not self.supabase:
            print(f"Supabase client not initialized, skipping download for {file_path}")
            return b""
            
        try:
            res = self.supabase.storage.from_(self.bucket_name).download(file_path)
            return res
        except Exception as e:
            raise StorageException(f"Failed to download file from storage: {str(e)}")
