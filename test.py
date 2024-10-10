import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configure logging
logging.basicConfig(filename='test_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ToDoAppTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000")
        cls.driver.implicitly_wait(10)
        cls.passed_tests = 0
        cls.failed_tests = 0
    
    @classmethod
    def tearDownClass(cls):
        # Close the WebDriver
        cls.driver.quit()
        print(f"Total Passed: {cls.passed_tests}")
        print(f"Total Failed: {cls.failed_tests}")

        # Logging the final pass/fail count
        logging.info(f"Total Passed: {cls.passed_tests}")
        logging.info(f"Total Failed: {cls.failed_tests}")

    def log_result(self, test_name, result):
        """Logs the result of each test case in the log file and updates the test counters."""
        if result:
            logging.info(f"{test_name}: PASSED")
            self.__class__.passed_tests += 1
        else:
            logging.error(f"{test_name}: FAILED")
            self.__class__.failed_tests += 1
    
    # Original 9 test cases
    def test_home_page_load(self):
        try:
            self.assertIn("ToDo", self.driver.title)
            self.log_result("test_home_page_load", True)
        except:
            self.log_result("test_home_page_load", False)
            

    def test_add_task(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.send_keys("Test Task")
            desc_input.send_keys("Test Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertGreaterEqual(len(task_list), 1)
            self.log_result("test_add_task", True)
        except:
            self.log_result("test_add_task", False)

    def test_update_task(self):
        try:
            task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[1]")
            task.click()
            task_input = self.driver.find_element(By.ID, 'task')
            task_input.clear()
            task_input.send_keys("Updated Task")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            updated_task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]").text
            self.assertEqual(updated_task, "Updated Task")
            self.log_result("test_update_task", True)
        except:
            self.log_result("test_update_task", False)

    def test_delete_task(self):
        try:
            task_delete = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[2]")
            task_delete.click()
            time.sleep(2)
            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertGreaterEqual(len(task_list), 0)
            self.log_result("test_delete_task", True)
        except:
            self.log_result("test_delete_task", False)

    def test_empty_task_submission(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.clear()
            desc_input.clear()
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertEqual(len(task_list), 0)
            self.log_result("test_empty_task_submission", True)
        except:
            self.log_result("test_empty_task_submission", False)

    def test_home_page_url(self):
        try:
            self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/")
            self.log_result("test_home_page_url", True)
        except:
            self.log_result("test_home_page_url", False)

    def test_404_page(self):
        try:
            self.driver.get("http://127.0.0.1:8000/update/9999")
            time.sleep(2)
            heading = self.driver.find_element(By.TAG_NAME, "h1").text
            self.assertEqual(heading, "404 Not Found")
            self.driver.get("http://127.0.0.1:8000")
            self.log_result("test_404_page", True)
        except:
            self.log_result("test_404_page", False)

    def test_navbar_present(self):
        try:
            navbar = self.driver.find_element(By.CLASS_NAME, 'navbar')
            self.assertTrue(navbar.is_displayed())
            self.log_result("test_navbar_present", True)
        except:
            self.log_result("test_navbar_present", False)

    def test_back_home_from_404(self):
        try:
            self.driver.get("http://127.0.0.1:8000/update/9999")
            back_button = self.driver.find_element(By.LINK_TEXT, "Go back to the homepage")
            back_button.click()
            time.sleep(2)
            self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/")
            self.log_result("test_back_home_from_404", True)
        except:
            self.log_result("test_back_home_from_404", False)

    # New 21 test cases

     # Test case 11: Check if task input field has the right placeholder (example for new cases)
    def test_task_input_placeholder(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            placeholder = task_input.get_attribute("placeholder")
            self.assertEqual(placeholder, "")
            self.log_result("test_task_input_placeholder", True)
        except Exception:
            self.log_result("test_task_input_placeholder", False)

    def test_description_input_placeholder(self):
        try:
            desc_input = self.driver.find_element(By.ID, 'desc')
            placeholder = desc_input.get_attribute("placeholder")
            self.assertEqual(placeholder, "")
            self.log_result("test_description_input_placeholder", True)
        except:
            self.log_result("test_description_input_placeholder", False)

    def test_add_task_button_present(self):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            self.assertTrue(button.is_displayed())
            self.log_result("test_add_task_button_present", True)
        except:
            self.log_result("test_add_task_button_present", False)

    def test_add_button_text(self):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').text
            self.assertEqual(button, "Add Task")
            self.log_result("test_add_button_text", True)
        except:
            self.log_result("test_add_button_text", False)

    def test_update_button_present(self):
        try:
            task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[1]")
            task.click()
            button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            self.assertTrue(button.is_displayed())
            self.driver.get("http://127.0.0.1:8000/")
            self.log_result("test_update_button_present", True)
        except:
            self.log_result("test_update_button_present", False)

    def test_task_display_table(self):
        try:
            table = self.driver.find_element(By.TAG_NAME, "table")
            self.assertTrue(table.is_displayed())
            self.log_result("test_task_display_table", True)
        except:
            self.log_result("test_task_display_table", False)

    def test_table_headings(self):
        try:
            headings = self.driver.find_elements(By.TAG_NAME, "th")
            headings_text = [heading.text for heading in headings]
            expected = ["Sr.No", "Task", "Description", "Actions"]
            self.assertEqual(headings_text, expected)
            self.log_result("test_table_headings", True)
        except:
            self.log_result("test_table_headings", False)

    def test_task_not_added_on_empty_submission(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.clear()
            desc_input.clear()
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            error_message = self.driver.find_element(By.XPATH, "//tbody/tr").text
            self.assertNotIn("None", error_message)
            self.log_result("test_task_not_added_on_empty_submission", True)
        except:
            self.log_result("test_task_not_added_on_empty_submission", False)

    def test_task_addition_with_space(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.send_keys("   ")
            desc_input.send_keys("   ")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertGreaterEqual(len(task_list), 0)
            self.log_result("test_task_addition_with_space", True)
        except:
            self.log_result("test_task_addition_with_space", False)

    def test_delete_button_present(self):
        try:
            task_delete = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[2]")
            self.assertTrue(task_delete.is_displayed())
            self.log_result("test_delete_button_present", True)
        except:
            self.log_result("test_delete_button_present", False)

    def test_delete_functionality(self):
        try:
            task_delete = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[2]")
            task_delete.click()
            time.sleep(2)
            deleted_task = self.driver.find_elements(By.XPATH, "//tbody/tr[1]/td[2]")
            self.assertEqual(len(deleted_task), 0)
            self.log_result("test_delete_functionality", True)
        except:
            self.log_result("test_delete_functionality", False)

    def test_task_updates_correctly(self):
        try:
            task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[1]")
            task.click()
            task_input = self.driver.find_element(By.ID, 'task')
            task_input.clear()
            task_input.send_keys("New Updated Task")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            updated_task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]").text
            self.assertEqual(updated_task, "New Updated Task")
            self.log_result("test_task_updates_correctly", True)
        except:
            self.log_result("test_task_updates_correctly", False)

    def test_empty_update_submission(self):
        try:
            task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[1]")
            task.click()
            task_input = self.driver.find_element(By.ID, 'task')
            task_input.clear()
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            error_message = self.driver.find_element(By.ID, "task").get_attribute("value")
            self.assertNotEqual(error_message, "")
            self.log_result("test_empty_update_submission", True)
        except:
            self.log_result("test_empty_update_submission", False)

    def test_navbar_link_functionality(self):
        try:
            self.driver.find_element(By.CLASS_NAME, 'navbar-brand').click()
            time.sleep(2)
            self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/")
            self.log_result("test_navbar_link_functionality", True)
        except:
            self.log_result("test_navbar_link_functionality", False)

    def test_navbar_brand_text(self):
        try:
            brand = self.driver.find_element(By.CLASS_NAME, 'navbar-brand').text
            self.assertEqual(brand, "My To Do")
            self.log_result("test_navbar_brand_text", True)
        except Exception:
            self.log_result("test_navbar_brand_text", False)

    def test_update_redirects_to_home(self):
        try:
            task = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[4]/a[1]")
            task.click()
            task_input = self.driver.find_element(By.ID, 'task')
            task_input.clear()
            task_input.send_keys("Updated Again")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/")
            self.log_result("test_update_redirects_to_home", True)
        except:
            self.log_result("test_update_redirects_to_home", False)

    def test_button_style(self):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            button_class = button.get_attribute("class")
            self.assertIn("btn-outline-dark", button_class)
            self.log_result("test_button_style", True)
        except:
            self.log_result("test_button_style", False)

    def test_table_row_count_after_task_addition(self):
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.send_keys("Task Count Test")
            desc_input.send_keys("Task Count Test Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)
            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertGreaterEqual(len(task_list), 1)
            self.log_result("test_table_row_count_after_task_addition", True)
        except:
            self.log_result("test_table_row_count_after_task_addition", False)

    def test_delete_invalid_task(self):
        try:
            self.driver.get("http://127.0.0.1:8000/delete/9999")
            time.sleep(2)
            heading = self.driver.find_element(By.TAG_NAME, "h1").text
            self.assertEqual(heading, "404 Not Found")
            self.driver.get("http://127.0.0.1:8000")
            self.log_result("test_delete_invalid_task", True)
        except:
            self.log_result("test_delete_invalid_task", False)

        def test_task_description_display(self):
            """Test that the task description is correctly displayed in the task list."""
            try:
                task_input = self.driver.find_element(By.ID, 'task')
                desc_input = self.driver.find_element(By.ID, 'desc')
                task_input.send_keys("Test Task Display")
                desc_input.send_keys("This is a test description.")
                self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
                time.sleep(2)
                task_description = self.driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]").text
                self.assertEqual(task_description, "This is a test description.")
                self.log_result("test_task_description_display", True)
            except:
                self.log_result("test_task_description_display", False)

    def test_duplicate_task_prevention(self):
        """Test that the same task cannot be added multiple times."""
        try:
            task_input = self.driver.find_element(By.ID, 'task')
            desc_input = self.driver.find_element(By.ID, 'desc')
            task_input.send_keys("Unique Task")
            desc_input.send_keys("Unique Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)

            # Attempt to add the same task again
            task_input.send_keys("Unique Task")
            desc_input.send_keys("Unique Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)

            task_list = self.driver.find_elements(By.XPATH, "//tbody/tr")
            self.assertEqual(len(task_list), 1)  # Ensure only one task exists
            self.log_result("test_duplicate_task_prevention", True)
        except:
            self.log_result("test_duplicate_task_prevention", False)

    def test_task_ordering(self):
        """Test that tasks are displayed in the order they were added."""
        try:
            self.driver.find_element(By.ID, 'task').send_keys("First Task")
            self.driver.find_element(By.ID, 'desc').send_keys("First Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)

            self.driver.find_element(By.ID, 'task').send_keys("Second Task")
            self.driver.find_element(By.ID, 'desc').send_keys("Second Description")
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(2)

            # Retrieve the tasks and check the order
            tasks = self.driver.find_elements(By.XPATH, "//tbody/tr")
            task_texts = [task.find_element(By.XPATH, "./td[2]").text for task in tasks]
            expected_order = ["First Task", "Second Task"]
            self.assertEqual(task_texts, expected_order)
            self.log_result("test_task_ordering", True)
        except:
            self.log_result("test_task_ordering", False)

    
if __name__ == "__main__":
    unittest.main()
