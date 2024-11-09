import unittest
from agents.user_interaction_agent import UserPreferences

class TestUserInteractionAgent(unittest.TestCase):
    def test_preferences(self):
        # Test: Creating a UserPreferences instance with valid data
        user_pref = UserPreferences(city="Paris", start_time="09:00", end_time="17:00", budget=100.0, interests=["Art", "Food"])

        # Check if the data is correctly assigned
        self.assertEqual(user_pref.city, "Paris")
        self.assertEqual(user_pref.start_time, "09:00")
        self.assertEqual(user_pref.end_time, "17:00")
        self.assertEqual(user_pref.budget, 100.0)
        self.assertEqual(user_pref.interests, ["Art", "Food"])

    def test_invalid_budget(self):
        # Test: Creating a UserPreferences instance with an invalid budget (negative value)
        with self.assertRaises(ValueError):
            UserPreferences(city="Rome", start_time="10:00", end_time="18:00", budget=-50.0, interests=["History"])

    def test_missing_field(self):
        # Test: Creating a UserPreferences instance with a missing field (city)
        with self.assertRaises(ValueError):
            UserPreferences(start_time="08:00", end_time="16:00", budget=80.0, interests=["Culture"])

    def test_invalid_time_format(self):
        # Test: Creating a UserPreferences instance with an invalid time format
        with self.assertRaises(ValueError):
            UserPreferences(city="Berlin", start_time="25:00", end_time="17:00", budget=120.0, interests=["Music"])

    def test_interests_type(self):
        # Test: Ensuring that interests must be a list
        with self.assertRaises(ValueError):
            UserPreferences(city="London", start_time="10:00", end_time="18:00", budget=150.0, interests="Art, Food")

    def test_equal_preferences(self):
        # Test: Check equality of two UserPreferences objects
        user_pref_1 = UserPreferences(city="Paris", start_time="09:00", end_time="17:00", budget=100.0, interests=["Art", "Food"])
        user_pref_2 = UserPreferences(city="Paris", start_time="09:00", end_time="17:00", budget=100.0, interests=["Art", "Food"])
        
        self.assertEqual(user_pref_1, user_pref_2)

    def test_non_equal_preferences(self):
        # Test: Check inequality of two UserPreferences objects with different values
        user_pref_1 = UserPreferences(city="Paris", start_time="09:00", end_time="17:00", budget=100.0, interests=["Art", "Food"])
        user_pref_2 = UserPreferences(city="Berlin", start_time="10:00", end_time="18:00", budget=150.0, interests=["Music"])

        self.assertNotEqual(user_pref_1, user_pref_2)


if __name__ == "__main__":
    unittest.main()
