import contextlib
import io
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

from parking_fee import minutes_parked, hourly_rate, format_plate


class CodeCoverageParkingFeeTests(unittest.TestCase):
    def test_minutes_parked(self):
        self.assertEqual(minutes_parked("09:30-11:45"), 135)

    def test_hourly_rate(self):
        self.assertEqual(hourly_rate(" CAR "), 30)

    def test_format_plate(self):
        self.assertEqual(format_plate("ka01ab1234"), "KA 01 AB 1234")

    def test_application_entry_point(self):
        script = Path(__file__).with_name("parking_fee.py")
        inputs = ["09:30-11:45", "bike", "ka01ab1234"]
        output = io.StringIO()

        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(script), run_name="__main__")

        result = output.getvalue()
        self.assertIn("Minutes Parked: 135", result)
        self.assertIn("Hourly Rate: 10", result)
        self.assertIn("Formatted Plate: KA 01 AB 1234", result)


if __name__ == "__main__":
    unittest.main()
