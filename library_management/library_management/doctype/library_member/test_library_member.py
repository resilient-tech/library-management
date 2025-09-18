# Copyright (c) 2025, Resilient Tech and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, nowdate

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestLibraryMember(IntegrationTestCase):
	"""
	Integration tests for LibraryMember.
	Use this class for testing interactions between multiple components.
	"""

	def test_member_creation_success(self):
		"""Test successful member creation with valid data"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "Member",
				"email": "test.member@example.com",
				"phone": "1234567890",
				"member_type": "Student",
				"membership_status": "Active",
				"max_books_allowed": 5,
			}
		)

		# Should save without errors
		member.insert()
		self.assertTrue(member.name)
		self.assertEqual(member.current_books_issued, 0)
		self.assertEqual(member.total_fines, 0)

		# Check auto-set membership dates
		self.assertEqual(member.membership_start_date, nowdate())
		self.assertEqual(member.membership_end_date, add_days(nowdate(), 365))

	def test_member_validation_missing_first_name(self):
		"""Test that member creation fails without first name"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"last_name": "Member",
				"email": "test@example.com",
				"member_type": "Student",
			}
		)

		with self.assertRaises(frappe.MandatoryError):
			member.insert()

	def test_member_validation_missing_last_name(self):
		"""Test that member creation fails without last name"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"email": "test@example.com",
				"member_type": "Student",
			}
		)

		with self.assertRaises(frappe.MandatoryError):
			member.insert()

	def test_member_validation_duplicate_email(self):
		"""Test that member creation fails with duplicate email"""
		# Create first member
		member1 = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "Member1",
				"email": "duplicate@example.com",
				"member_type": "Student",
			}
		)
		member1.insert()

		# Try to create second member with same email
		member2 = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "Member2",
				"email": "duplicate@example.com",  # Duplicate email
				"member_type": "Faculty",
			}
		)

		with self.assertRaises(frappe.UniqueValidationError) as context:
			member2.insert()

		self.assertIn("duplicate@example.com", str(context.exception))

	def test_member_get_full_name(self):
		"""Test the get_full_name method"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "John",
				"last_name": "Doe",
				"email": "john.doe@example.com",
				"member_type": "Student",
			}
		)
		member.insert()

		self.assertEqual(member.get_full_name(), "John Doe")

	def test_member_default_membership_dates(self):
		"""Test auto-setting of membership dates"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "DateMember",
				"email": "testdate@example.com",
				"member_type": "Student",
			}
		)
		member.insert()

		# Check default dates
		self.assertEqual(member.membership_start_date, nowdate())
		self.assertEqual(member.membership_end_date, add_days(nowdate(), 365))

	def test_member_custom_membership_dates(self):
		"""Test setting custom membership dates"""
		start_date = add_days(nowdate(), 10)
		end_date = add_days(nowdate(), 375)

		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "CustomDate",
				"email": "customdate@example.com",
				"member_type": "Faculty",
				"membership_start_date": start_date,
				"membership_end_date": end_date,
			}
		)
		member.insert()

		# Should keep custom dates
		self.assertEqual(member.membership_start_date, start_date)
		self.assertEqual(member.membership_end_date, end_date)

	def test_member_books_issued_calculation(self):
		"""Test that current_books_issued is calculated correctly"""
		member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Test",
				"last_name": "BooksIssued",
				"email": "testbooksissued@example.com",
				"member_type": "Student",
			}
		)
		member.insert()

		# Initially should be 0
		self.assertEqual(member.current_books_issued, 0)
