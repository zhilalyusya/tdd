from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_for_one_user(self):
		#Inong has heard about a cool new online to-do app. 
		# She goes to check out its homepage
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# She types "Buy peacock feathers" into a text box (Inong's hobby
		# is tying fly-fishing lures)
		inputbox.send_keys('Buy peacock feathers')

		# When she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Inong is very methodical)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Use peacock feathers to make a fly')		
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on her list
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Inong starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# She notices that her list has a unique URL
		inong_list_url = self.browser.current_url
		self.assertRegex(inong_list_url, '/lists/.+')

		# Now a new user, Agam comes along to the site

		## Use a new browser session to make sure that no information
		## of Inong's is coming through from cookies etc
		self.browser.quit()
		# self.browser = webdriver.Firefox()
		self.browser = webdriver.Chrome()

		# Agam visits the home page. There is no sign of Inong's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Agam starts a new list by entering a new item. He
		# is less interesting than Inong...
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Agam gets his own unique URL
		agam_list_url = self.browser.current_url
		self.assertRegex(agam_list_url, '/lists/.+')
		self.assertNotEqual(agam_list_url, inong_list_url)

		# Again, there is no trace of Inong's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfied, they both go back to sleep 