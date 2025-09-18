# Copyright (c) 2025, Resilient Tech and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import nowdate

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestBook(IntegrationTestCase):
	"""
	Integration tests for Book.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		"""Set up test data before each test"""
		self.create_test_dependencies()

	def create_test_dependencies(self):
		"""Create necessary test records for Book"""
		# Create Author
		if not frappe.db.exists("Author", "Test Author"):
			frappe.get_doc(
				{"doctype": "Author", "author_name": "Test Author", "biography": "Test biography"}
			).insert(ignore_permissions=True)

		# Create Publisher
		if not frappe.db.exists("Publisher", "Test Publisher"):
			frappe.get_doc(
				{"doctype": "Publisher", "publisher_name": "Test Publisher", "address": "Test Address"}
			).insert(ignore_permissions=True)

		# Create Language
		if not frappe.db.exists("Language", "en"):
			frappe.get_doc({"doctype": "Language", "language_name": "en"}).insert(ignore_permissions=True)

		# Create Book Category
		if not frappe.db.exists("Book Category", "Fiction"):
			frappe.get_doc({"doctype": "Book Category", "category_name": "Fiction"}).insert(
				ignore_permissions=True
			)

		# Create Library Location
		if not frappe.db.exists("Library Location", "Test Location"):
			frappe.get_doc(
				{
					"doctype": "Library Location",
					"location_name": "Test Location",
					"floor": "Ground Floor",
					"section": "A",
				}
			).insert(ignore_permissions=True)

	def test_book_creation_success(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Success",
				"isbn": "978-1234567890",
				"publisher": "Test Publisher",
				"language": "en",
				"book_category": "Fiction",
				"location": "Test Location",
				"total_copies": 5,
				"price": 299.0,
				"acquisition_date": nowdate(),
				"condition": "New",
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 100}
				],
			}
		)

		# Should save without errors
		book.insert()
		self.assertTrue(book.name)
		self.assertEqual(book.available_copies, 5)

	def test_book_validation_no_authors(self):
		book = frappe.get_doc(
			{"doctype": "Book", "title": "Test Book No Authors", "total_copies": 5, "authors": []}
		)

		with self.assertRaises(frappe.ValidationError):
			book.insert()

	def test_book_validation_invalid_contribution(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Invalid Contribution",
				"total_copies": 5,
				"authors": [
					{
						"author": "Test Author",
						"author_type": "Primary",
						"contribution_percentage": 50,  # Should be 100% for single author
					}
				],
			}
		)

		with self.assertRaises(frappe.ValidationError):
			book.insert()

	def test_book_validation_duplicate_authors(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Duplicate Authors",
				"total_copies": 5,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 50},
					{
						"author": "Test Author",  # Duplicate
						"author_type": "Secondary",
						"contribution_percentage": 50,
					},
				],
			}
		)

		with self.assertRaises(frappe.ValidationError):
			book.insert()

	def test_book_validation_zero_copies(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Zero Copies",
				"total_copies": 0,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 100}
				],
			}
		)

		with self.assertRaises(frappe.ValidationError):
			book.insert()

	def test_book_validation_negative_copies(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Negative Copies",
				"total_copies": -5,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 100}
				],
			}
		)

		with self.assertRaises(frappe.ValidationError):
			book.insert()

	def test_multiple_authors_valid_contribution(self):
		# Create second author
		if not frappe.db.exists("Author", "Secondary Test"):
			frappe.get_doc({"doctype": "Author", "author_name": "Secondary Test"}).insert(
				ignore_permissions=True
			)

		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Multiple Authors",
				"total_copies": 3,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 60},
					{"author": "Secondary Test", "author_type": "Secondary", "contribution_percentage": 40},
				],
			}
		)

		# Should save successfully
		book.insert()
		self.assertTrue(book.name)
		self.assertEqual(len(book.authors), 2)

	def test_book_is_available_method(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Availability",
				"total_copies": 5,
				"is_reference_only": 0,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 100}
				],
			}
		)
		book.insert()

		# Should be available
		self.assertTrue(book.is_available())

		# Set as reference only
		book.is_reference_only = 1
		book.save()

		# Should not be available for issue
		self.assertFalse(book.is_available())

	def test_book_available_copies_calculation(self):
		book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Book Available Copies",
				"total_copies": 5,
				"authors": [
					{"author": "Test Author", "author_type": "Primary", "contribution_percentage": 100}
				],
			}
		)
		book.insert()
		self.assertEqual(book.available_copies, book.total_copies)
