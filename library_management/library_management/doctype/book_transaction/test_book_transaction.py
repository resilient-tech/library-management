# Copyright (c) 2025, Resilient Tech and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, getdate, nowdate

from library_management.library_management.doctype.book_transaction.book_transaction import (
	get_issued_book_count,
	get_total_fines,
)

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestBookTransaction(IntegrationTestCase):
	"""
	Integration tests for BookTransaction.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		"""Set up test data before each test"""
		self.create_test_dependencies()

	def create_test_dependencies(self):
		"""Create necessary test records for Book Transaction"""
		# Create Library Settings
		if not frappe.db.exists("Library Settings", "Library Settings"):
			settings = frappe.get_doc(
				{
					"doctype": "Library Settings",
					"default_issue_period": 14,
					"fine_per_day": 2.0,
					"max_books_per_member": 5,
				}
			)
			settings.insert(ignore_permissions=True)

		# Create Author
		if not frappe.db.exists("Author", "Test Transaction Author"):
			frappe.get_doc({"doctype": "Author", "author_name": "Test Transaction Author"}).insert(
				ignore_permissions=True
			)

		# Create Publisher
		if not frappe.db.exists("Publisher", "Test Transaction Publisher"):
			frappe.get_doc({"doctype": "Publisher", "publisher_name": "Test Transaction Publisher"}).insert(
				ignore_permissions=True
			)

		# Create Language
		if not frappe.db.exists("Language", "en"):
			frappe.get_doc({"doctype": "Language", "language_name": "en"}).insert(ignore_permissions=True)

		# Create Book Category
		if not frappe.db.exists("Book Category", "Test Category"):
			frappe.get_doc({"doctype": "Book Category", "category_name": "Test Category"}).insert(
				ignore_permissions=True
			)

		# Create Library Location
		if not frappe.db.exists("Library Location", "Test Transaction Location"):
			frappe.get_doc(
				{
					"doctype": "Library Location",
					"location_name": "Test Transaction Location",
					"floor": "Ground Floor",
					"section": "A",
				}
			).insert(ignore_permissions=True)

		# Create Test Book
		if not frappe.db.exists("Book", None, {"title": "Test Transaction Book"}):
			book = frappe.get_doc(
				{
					"doctype": "Book",
					"title": "Test Transaction Book",
					"isbn": "978-1234567891",
					"publisher": "Test Transaction Publisher",
					"language": "en",
					"book_category": "Test Category",
					"location": "Test Transaction Location",
					"total_copies": 3,
					"price": 299.0,
					"condition": "New",
					"authors": [
						{
							"author": "Test Transaction Author",
							"author_type": "Primary",
							"contribution_percentage": 100,
						}
					],
				}
			)
			book.insert(ignore_permissions=True)
			self.test_book_name = book.name

		# Create Test Member
		if not frappe.db.exists("Library Member", None, {"email": "testtransaction@example.com"}):
			member = frappe.get_doc(
				{
					"doctype": "Library Member",
					"first_name": "Test",
					"last_name": "Transaction",
					"email": "testtransaction@example.com",
					"member_type": "Student",
					"membership_status": "Active",
					"max_books_allowed": 3,
				}
			)
			member.insert(ignore_permissions=True)
			self.test_member_name = member.name

	def get_test_book(self):
		"""Get test book name"""
		if hasattr(self, "test_book_name"):
			return self.test_book_name
		return frappe.db.get_value("Book", {"title": "Test Transaction Book"}, "name")

	def get_test_member(self):
		"""Get test member name"""
		if hasattr(self, "test_member_name"):
			return self.test_member_name
		return frappe.db.get_value("Library Member", {"email": "testtransaction@example.com"}, "name")

	def test_issue_transaction_success(self):
		"""Test successful book issue transaction"""
		transaction = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"transaction_date": nowdate(),
				"condition_on_issue": "Good",
			}
		)

		# Should save and submit successfully
		transaction.insert()
		transaction.submit()

		self.assertTrue(transaction.name)
		self.assertEqual(transaction.docstatus, 1)
		self.assertTrue(transaction.due_date)
		self.assertEqual(transaction.due_date, add_days(getdate(transaction.transaction_date), 14))

	def test_return_transaction_success(self):
		"""Test successful book return transaction"""
		# First create an issue transaction
		issue_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"transaction_date": add_days(nowdate(), -10),
				"due_date": add_days(nowdate(), 4),
				"condition_on_issue": "Good",
			}
		)
		issue_txn.insert()
		issue_txn.submit()

		# Now create return transaction
		return_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Return",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"transaction_date": nowdate(),
				"return_date": nowdate(),
				"condition_on_return": "Good",
				"fine_amount": 0,
			}
		)

		# Should save successfully
		return_txn.insert()
		return_txn.submit()

		self.assertTrue(return_txn.name)
		self.assertEqual(return_txn.docstatus, 1)

	def test_member_inactive_validation(self):
		"""Test that inactive members cannot issue books"""
		# Create inactive member
		inactive_member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Inactive",
				"last_name": "Member",
				"email": "inactive@example.com",
				"member_type": "Student",
				"membership_status": "Suspended",
				"max_books_allowed": 3,
			}
		)
		inactive_member.insert(ignore_permissions=True)

		transaction = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": inactive_member.name,
				"book": self.get_test_book(),
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			transaction.insert()

	def test_expired_membership_validation(self):
		"""Test that members with expired membership cannot issue books"""
		# Create member with expired membership
		expired_member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Expired",
				"last_name": "Member",
				"email": "expired@example.com",
				"member_type": "Student",
				"membership_status": "Active",
				"membership_start_date": add_days(nowdate(), -400),
				"membership_end_date": add_days(nowdate(), -10),  # Expired
				"max_books_allowed": 3,
			}
		)
		expired_member.insert(ignore_permissions=True)

		transaction = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": expired_member.name,
				"book": self.get_test_book(),
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			transaction.insert()

		# Clean up
		expired_member.delete()

	def test_reference_book_validation(self):
		"""Test that reference books cannot be issued"""
		# Create reference book
		ref_book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Reference Book",
				"isbn": "978-1234567892",
				"publisher": "Test Transaction Publisher",
				"language": "en",
				"book_category": "Test Category",
				"location": "Test Transaction Location",
				"total_copies": 2,
				"is_reference_only": 1,  # Reference book
				"condition": "New",
				"authors": [
					{
						"author": "Test Transaction Author",
						"author_type": "Primary",
						"contribution_percentage": 100,
					}
				],
			}
		)
		ref_book.insert(ignore_permissions=True)

		transaction = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": self.get_test_member(),
				"book": ref_book.name,
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			transaction.insert()

	def test_book_availability_validation(self):
		# Create book with only 1 copy
		single_book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Single Copy Book",
				"isbn": "978-1234567893",
				"publisher": "Test Transaction Publisher",
				"language": "en",
				"book_category": "Test Category",
				"location": "Test Transaction Location",
				"total_copies": 1,
				"condition": "New",
				"authors": [
					{
						"author": "Test Transaction Author",
						"author_type": "Primary",
						"contribution_percentage": 100,
					}
				],
			}
		)
		single_book.insert(ignore_permissions=True)

		# Issue the only copy
		first_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": self.get_test_member(),
				"book": single_book.name,
				"condition_on_issue": "Good",
			}
		)
		first_txn.insert()
		first_txn.submit()

		# Create second member to try issuing the same book
		second_member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Second",
				"last_name": "Member",
				"email": "second@example.com",
				"member_type": "Student",
				"membership_status": "Active",
				"max_books_allowed": 3,
			}
		)
		second_member.insert(ignore_permissions=True)

		# Try to issue the same book (should fail)
		second_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": second_member.name,
				"book": single_book.name,
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			second_txn.insert()

	def test_member_book_limit_validation(self):
		# Create member with limit of 1 book
		limited_member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Limited",
				"last_name": "Member",
				"email": "limited@example.com",
				"member_type": "Student",
				"membership_status": "Active",
				"max_books_allowed": 1,
			}
		)
		limited_member.insert(ignore_permissions=True)

		# Create additional book
		second_book = frappe.get_doc(
			{
				"doctype": "Book",
				"title": "Test Second Book",
				"isbn": "978-1234567894",
				"publisher": "Test Transaction Publisher",
				"language": "en",
				"book_category": "Test Category",
				"location": "Test Transaction Location",
				"total_copies": 2,
				"condition": "New",
				"authors": [
					{
						"author": "Test Transaction Author",
						"author_type": "Primary",
						"contribution_percentage": 100,
					}
				],
			}
		)
		second_book.insert(ignore_permissions=True)

		# Issue first book
		first_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": limited_member.name,
				"book": self.get_test_book(),
				"condition_on_issue": "Good",
			}
		)
		first_txn.insert()
		first_txn.submit()

		# Try to issue second book (should fail)
		second_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": limited_member.name,
				"book": second_book.name,
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			second_txn.insert()
			second_txn.submit()

	def test_outstanding_fines_validation(self):
		# Create member with fines
		fined_member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Fined",
				"last_name": "Member",
				"email": "fined@example.com",
				"member_type": "Student",
				"membership_status": "Active",
				"max_books_allowed": 3,
			}
		)
		fined_member.insert(ignore_permissions=True)

		# Create a completed transaction with fine
		fine_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Return",
				"member": fined_member.name,
				"book": self.get_test_book(),
				"transaction_date": add_days(nowdate(), -20),
				"due_date": add_days(nowdate(), -10),
				"return_date": add_days(nowdate(), -5),
				"fine_amount": 10.0,
				"fine_paid": 0,  # Fine not paid
				"condition_on_issue": "Good",
				"condition_on_return": "Good",
			}
		)
		fine_txn.insert()
		fine_txn.submit()

		# Try to issue new book (should fail due to outstanding fine)
		new_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": fined_member.name,
				"book": self.get_test_book(),
				"condition_on_issue": "Good",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			new_txn.insert()
			new_txn.submit()

	def test_fine_calculation_overdue(self):
		return_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Return",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"transaction_date": add_days(nowdate(), -20),
				"due_date": add_days(nowdate(), -10),  # Due 10 days ago
				"return_date": add_days(nowdate(), -5),  # Returned 5 days late
				"condition_on_issue": "Good",
				"condition_on_return": "Good",
			}
		)

		return_txn.insert()

		# Fine should be calculated: 5 days * 2.0 per day = 10.0
		expected_fine = 5 * 2.0
		self.assertEqual(return_txn.fine_amount, expected_fine)

	def test_fine_calculation_on_time(self):
		"""Test that no fine is calculated for on-time returns"""
		return_txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Return",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"transaction_date": add_days(nowdate(), -10),
				"due_date": add_days(nowdate(), 4),  # Due in future
				"return_date": nowdate(),  # Returning on time
				"condition_on_issue": "Good",
				"condition_on_return": "Good",
			}
		)

		return_txn.insert()

		# No fine should be calculated
		self.assertEqual(return_txn.fine_amount, 0)

	def test_get_issued_book_count_function(self):
		member = self.get_test_member()
		book = self.get_test_book()

		# Initially should be 0
		self.assertEqual(get_issued_book_count(member=member), 0)
		self.assertEqual(get_issued_book_count(book=book), 0)

		# Issue a book
		txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": member,
				"book": book,
				"condition_on_issue": "Good",
			}
		)
		txn.insert()
		txn.submit()

		# Should now return 1
		self.assertEqual(get_issued_book_count(member=member), 1)
		self.assertEqual(get_issued_book_count(book=book), 1)

	def test_get_total_fines_function(self):
		member = self.get_test_member()

		# Initially should be 0
		self.assertEqual(get_total_fines(member), 0)

		# Create transaction with fine
		txn = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Return",
				"member": member,
				"book": self.get_test_book(),
				"transaction_date": add_days(nowdate(), -20),
				"due_date": add_days(nowdate(), -10),
				"return_date": add_days(nowdate(), -5),
				"fine_paid": 0,
				"condition_on_issue": "Good",
				"condition_on_return": "Good",
			}
		)
		txn.insert()
		txn.submit()

		# Should return the fine amount
		self.assertEqual(get_total_fines(member), 10.0)  # 5 days * 2.0 per day

	def test_default_values_setting(self):
		transaction = frappe.get_doc(
			{
				"doctype": "Book Transaction",
				"transaction_type": "Issue",
				"member": self.get_test_member(),
				"book": self.get_test_book(),
				"condition_on_issue": "Good",
				# Note: Not setting transaction_date or due_date
			}
		)

		transaction.insert()

		# Should auto-set transaction_date and due_date
		self.assertTrue(transaction.transaction_date)
		self.assertTrue(transaction.due_date)
		self.assertEqual(transaction.due_date, add_days(getdate(transaction.transaction_date), 14))

		transaction.delete()

	def tearDown(self):
		frappe.db.sql(
			"DELETE FROM `tabBook Transaction` WHERE member IN (SELECT name FROM `tabLibrary Member` WHERE email LIKE '%example.com')"
		)
		frappe.db.sql("DELETE FROM `tabLibrary Member` WHERE email LIKE '%example.com'")
		frappe.db.sql("DELETE FROM `tabBook` WHERE title LIKE 'Test %'")

		frappe.db.commit()
