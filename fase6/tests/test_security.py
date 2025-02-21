import unittest
from security.threat_detector import ThreatDetector

class TestSecurity(unittest.TestCase):
    def test_threat_detection(self):
        detector = ThreatDetector()
        threats = detector.scan("eval('1+1')")
        self.assertIn("eval", threats[0])