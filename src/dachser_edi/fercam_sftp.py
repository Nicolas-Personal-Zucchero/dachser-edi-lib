import os
import io
import paramiko
import logging
from typing import Optional, Union
import posixpath

class FercamSFTP:
    _PRODUCTION_SERVER = "sftp-prod-in.fercam.com"
    _TEST_SERVER = "sftp-test-in.fercam.com"

    DIR_TO_FERCAM = "To_Fercam"
    DIR_FROM_FERCAM = "From_Fercam"

    def __init__(self, 
                username: str, 
                password: str, 
                use_test_server: bool = False, 
                auto_add_keys: bool = False,
                timeout: int = 30,
                logger: Optional[logging.Logger] = None
                ) -> None:
        self.username = username
        self.password = password
        self.hostname = self._TEST_SERVER if use_test_server else self._PRODUCTION_SERVER
        self.timeout = timeout

        self.logger = logger or logging.getLogger(__name__)

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        if auto_add_keys:
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.sftp: Optional[paramiko.SFTPClient] = None

    def __enter__(self):
        """Permette l'uso di 'with FercamSFTP(...) as sftp:'"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def connect(self) -> None:
        if self.sftp is None:
            try:
                self.logger.info(f"Connecting to {self.hostname}...")
                self.ssh_client.connect(
                    self.hostname, 
                    username=self.username, 
                    password=self.password,
                    timeout=self.timeout,
                    banner_timeout=30
                )
                self.sftp = self.ssh_client.open_sftp()
                self.logger.info("Connection established.")
            except Exception as e:
                self.logger.error(f"Failed to connect: {e}")
                raise

    def close(self):
        if self.sftp:
            self.sftp.close()
            self.sftp = None
        self.ssh_client.close()
        self.logger.info("Connection closed.")

    def _ensure_connection(self) -> None:
        """Verifica che il socket e il canale SFTP siano effettivamente attivi."""
        transport = self.ssh_client.get_transport()
        if self.sftp is None or transport is None or not transport.is_active():
            self.logger.info("Socket inattivo o disconnesso, tentativo di riconnessione...")
            self.connect()

    def send_file(self, local_file_path: str, remote_filename: str = None) -> None:
        self._ensure_connection()
        
        if not os.path.isfile(local_file_path):
            self.logger.error(f"Local file '{local_file_path}' not found.")
            raise FileNotFoundError(f"File not found: {local_file_path}")
        
        filename = remote_filename or os.path.basename(local_file_path)
        remote_file_path = posixpath.join(self.DIR_TO_FERCAM, filename)


        try:
            self.logger.info(f"Uploading {local_file_path} to {remote_file_path}...")

            # confirm=False because the file is immediately removed by Fercam after upload so a check would fail
            self.sftp.put(local_file_path, remote_file_path, confirm=False)
            
            self.logger.info("Upload successful.")
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            raise

    def send_content(self, content: Union[str, bytes], remote_filename: str) -> None:
        self._ensure_connection()

        remote_file_path = posixpath.join(self.DIR_TO_FERCAM, remote_filename)

        # Paramiko richiede stream di byte. Codifichiamo la stringa se necessario.
        if isinstance(content, str):
            content = content.encode('utf-8')
            
        file_obj = io.BytesIO(content)

        try:
            self.logger.info(f"Uploading in-memory content to {remote_file_path}...")
            
            # putfo gestisce i file-like objects (stream in memoria)
            # confirm=False because the file is immediately removed by Fercam after upload so a check would fail
            self.sftp.putfo(file_obj, remote_file_path, confirm=False)
            
            self.logger.info("Upload successful.")
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            raise

    def get_file(self, remote_filename: str, local_folder: str, delete_after: bool = False) -> None:
        self._ensure_connection()


        remote_path = posixpath.join(self.DIR_FROM_FERCAM, remote_filename)
        local_path = os.path.join(local_folder, remote_filename)

        try:
            self.logger.info(f"Downloading {remote_path} to {local_path}...")
            self.sftp.get(remote_path, local_path)
            self.logger.info("\nDownload successful.")

            if delete_after:
                self.logger.info(f"Removing remote file {remote_path}...")
                self.sftp.remove(remote_path)
                self.logger.info("Remote file removed.")

        except Exception as e:
            self.logger.error(f"Operation failed: {e}")
            if os.path.exists(local_path) and os.path.getsize(local_path) == 0:
                os.remove(local_path)
            raise