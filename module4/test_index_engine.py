"""
Unit tests for Module 4: Index Engine
Run with: python3 test_index_engine.py
"""

import unittest
from index_engine import IndexEngine


class TestIndexEngine(unittest.TestCase):
    def setUp(self):
        """Provides sample stock prices for STK_1 to STK_15."""
        self.sample_prices = {
            "STK_1": 100.0,
            "STK_2": 200.0,
            "STK_3": 150.0,
            "STK_4": 50.0,
            "STK_5": 300.0,
            "STK_6": 120.0,
            "STK_7": 80.0,
            "STK_8": 90.0,
            "STK_9": 110.0,
            "STK_10": 100.0,
            "STK_11": 75.0,
            "STK_12": 125.0,
            "STK_13": 150.0,
            "STK_14": 95.0,
            "STK_15": 210.0,
        }

    def test_index_tech_equal_weight(self):
        """
        Tests INDEX_TECH equal-weight calculation (w_i = 0.20 each for STK_1..5).
        Expected sum: (100*0.2) + (200*0.2) + (150*0.2) + (50*0.2) + (300*0.2) = 160.0
        """
        engine = IndexEngine()
        tech_price = engine.calculate_index_tech(self.sample_prices)
        self.assertAlmostEqual(tech_price, 160.0, places=3)
        print(f"PASSED: {self._testMethodName}")

    def test_index_tech_custom_weight(self):
        """
        Tests INDEX_TECH custom weight calculation.
        """
        custom_weights = {
            "STK_1": 0.40,
            "STK_2": 0.30,
            "STK_3": 0.10,
            "STK_4": 0.10,
            "STK_5": 0.10,
        }
        # Expected: (100*0.4) + (200*0.3) + (150*0.1) + (50*0.1) + (300*0.1)
        #         = 40 + 60 + 15 + 5 + 30 = 150.0
        engine = IndexEngine(tech_weights=custom_weights)
        tech_price = engine.calculate_index_tech(self.sample_prices)
        self.assertAlmostEqual(tech_price, 150.0, places=3)
        print(f"PASSED: {self._testMethodName}")

    def test_index_main_equal_weight(self):
        """
        Tests INDEX_MAIN calculation (equal average of STK_1 to STK_10).
        Sum(100 + 200 + 150 + 50 + 300 + 120 + 80 + 90 + 110 + 100) = 1300.0
        Average = 1300.0 / 10 = 130.0
        """
        engine = IndexEngine()
        main_price = engine.calculate_index_main(self.sample_prices)
        self.assertAlmostEqual(main_price, 130.0, places=3)
        print(f"PASSED: {self._testMethodName}")

    def test_on_price_tick_and_subscriber_notification(self):
        """
        Tests full tick update and cross-asset subscriber notifications.
        """
        engine = IndexEngine()
        received_updates = []

        # Mock subscriber function (simulating Module 2 or Module 3)
        def handle_index_update(index_data):
            received_updates.append(index_data)

        engine.register_subscriber(handle_index_update)

        result = engine.on_price_tick(self.sample_prices)

        self.assertAlmostEqual(result["INDEX_TECH"], 160.0, places=3)
        self.assertAlmostEqual(result["INDEX_MAIN"], 130.0, places=3)
        self.assertEqual(len(received_updates), 1)
        self.assertEqual(received_updates[0], result)
        print(f"PASSED: {self._testMethodName}")


if __name__ == "__main__":
    print("Running test suite...")
    unittest.main(verbosity=2)

