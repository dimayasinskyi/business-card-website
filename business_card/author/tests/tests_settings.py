from django.test import TestCase, override_settings
import tempfile, shutil


class MediaCleanTestCase(TestCase):
    def setUp(self):
        self._temp_media = tempfile.mkdtemp()
        self._override = override_settings(MEDIA_ROOT=self._temp_media)
        self._override.enable()

    def tearDown(self):
        self._override.disable()
        shutil.rmtree(self._temp_media, ignore_errors=True)
        
