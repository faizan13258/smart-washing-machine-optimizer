import unittest
import math

from src.product_predict import predict_one, validate_input


class TestProductPrediction(unittest.TestCase):

    def setUp(self):
        self.valid_input = {
            "dirt_level": 70,
            "load_kg": 5,
            "fabric_type": "Cotton",
            "water_availability": "Medium"
        }

    def test_1_normal_prediction(self):
        result = predict_one(self.valid_input)

        self.assertIn("inputs", result)
        self.assertIn("predictions", result)

        expected_outputs = [
            "wash_time_min",
            "water_consumption_l",
            "detergent_ml",
            "spin_speed_rpm"
        ]

        self.assertEqual(
            list(result["predictions"].keys()),
            expected_outputs
        )

        for value in result["predictions"].values():
            self.assertTrue(math.isfinite(value))

    def test_2_boundary_values(self):
        lower = self.valid_input.copy()
        lower["dirt_level"] = 0
        lower["load_kg"] = 0.1

        upper = self.valid_input.copy()
        upper["dirt_level"] = 100
        upper["load_kg"] = 10

        self.assertEqual(validate_input(lower)["dirt_level"], 0)
        self.assertEqual(validate_input(upper)["load_kg"], 10)

        self.assertEqual(len(predict_one(lower)["predictions"]), 4)
        self.assertEqual(len(predict_one(upper)["predictions"]), 4)

    def test_3_invalid_numeric_values(self):
        invalid_dirt = self.valid_input.copy()
        invalid_dirt["dirt_level"] = 101

        invalid_load = self.valid_input.copy()
        invalid_load["load_kg"] = -1

        with self.assertRaises(ValueError):
            validate_input(invalid_dirt)

        with self.assertRaises(ValueError):
            validate_input(invalid_load)

    def test_4_invalid_categories(self):
        invalid_fabric = self.valid_input.copy()
        invalid_fabric["fabric_type"] = "Unknown"

        invalid_water = self.valid_input.copy()
        invalid_water["water_availability"] = "Unknown"

        with self.assertRaises(ValueError):
            validate_input(invalid_fabric)

        with self.assertRaises(ValueError):
            validate_input(invalid_water)

    def test_5_missing_required_input(self):
        incomplete = self.valid_input.copy()
        del incomplete["fabric_type"]

        with self.assertRaises(ValueError):
            validate_input(incomplete)


if __name__ == "__main__":
    unittest.main()
