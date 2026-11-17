import contextlib
import io
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

# Importing the module executes the False outcome of the __main__ guard.
import parking_fee  # noqa: F401


class BranchCoverageParkingFeeTests(unittest.TestCase):
    def test_script_entry_point_true_branch(self):
        script = Path(__file__).with_name("parking_fee.py")
        inputs = ["09:30-11:45", "truck", "ka01ab1234"]
        output = io.StringIO()

        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(script), run_name="__main__")

        result = output.getvalue()
        self.assertIn("Minutes Parked: 135", result)
        self.assertIn("Hourly Rate: 60", result)
        self.assertIn("Formatted Plate: KA 01 AB 1234", result)


if __name__ == "__main__":
    unittest.main()
