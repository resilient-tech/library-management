#!/usr/bin/env python3
"""
Sample Data Generator for Library Management System
Creates comprehensive sample data with Indian references
"""

import random

import frappe
from frappe.utils import add_days, add_months, nowdate


def run():
	"""Main function to create sample data"""
	print("Starting sample data creation...")

	# Delete existing data first
	delete_existing_data()

	# Create data in dependency order
	create_library_settings()
	create_authors()
	create_publishers()
	create_book_categories()
	create_book_subcategories()
	create_library_locations()
	create_books()
	create_library_members()
	create_book_transactions()
	create_fee_collections()

	frappe.db.commit()
	print("Sample data creation completed successfully!")


def delete_existing_data():
	"""Delete all existing records to start fresh"""
	print("Deleting existing data...")

	# Delete in reverse dependency order
	doctypes_to_clear = [
		"Fee Collection",
		"Book Transaction",
		"Library Member",
		"Book",
		"Library Location",
		"Book Subcategory",
		"Book Category",
		"Publisher",
		"Author",
	]

	for doctype in doctypes_to_clear:
		frappe.db.sql(f"DELETE FROM `tab{doctype}`")
		print(f"Cleared {doctype}")


def create_library_settings():
	"""Create library settings configuration"""
	print("Creating Library Settings...")

	# Create the singles document
	doc = frappe.new_doc("Library Settings")
	doc.library_name = "Bharatiya Vigyan Bhavan Library"
	doc.max_books_per_member = 5
	doc.default_issue_period = 14
	doc.fine_per_day = 2.0
	doc.enable_reservations = 1
	doc.auto_extend_enabled = 0
	doc.email_notifications = 1
	doc.library_hours = []
	doc.save()

	# Add library hours
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	for day in days:
		doc.append(
			"library_hours",
			{
				"day_of_week": day,
				"is_open": 1,
				"opening_time": "09:00:00",
				"closing_time": "18:00:00",
				"break_start_time": "13:00:00",
				"break_end_time": "14:00:00",
			},
		)

	# Sunday - closed
	doc.append("library_hours", {"day_of_week": "Sunday", "is_open": 0})
	doc.save()

	print("Created Library Settings")


def create_authors():
	"""Create author records"""
	print("Creating Authors...")

	authors = [
		{
			"author_name": "Rabindranath Tagore",
			"biography": "Nobel Prize-winning Bengali polymath, poet, writer, playwright, composer, and philosopher.",
			"nationality": "Indian",
			"birth_date": "1861-05-07",
			"death_date": "1941-08-07",
		},
		{
			"author_name": "R.K. Narayan",
			"biography": "Indian writer known for his works set in the fictional South Indian town of Malgudi.",
			"nationality": "Indian",
			"birth_date": "1906-10-10",
			"death_date": "2001-05-13",
		},
		{
			"author_name": "Premchand",
			"biography": "Indian writer famous for his modern Hindi-Urdu literature.",
			"nationality": "Indian",
			"birth_date": "1880-07-31",
			"death_date": "1936-10-08",
		},
		{
			"author_name": "Satyajit Ray",
			"biography": "Indian filmmaker, screenwriter, author, and graphic designer.",
			"nationality": "Indian",
			"birth_date": "1921-05-02",
			"death_date": "1992-04-23",
		},
		{
			"author_name": "Vikram Seth",
			"biography": "Indian novelist and poet, author of A Suitable Boy.",
			"nationality": "Indian",
			"birth_date": "1952-06-20",
		},
		{
			"author_name": "Arundhati Roy",
			"biography": "Indian author and political activist, winner of the Booker Prize.",
			"nationality": "Indian",
			"birth_date": "1961-11-24",
		},
		{
			"author_name": "Kiran Desai",
			"biography": "Indian author and daughter of Anita Desai.",
			"nationality": "Indian",
			"birth_date": "1971-09-03",
		},
		{
			"author_name": "Salman Rushdie",
			"biography": "British-Indian novelist and essayist.",
			"nationality": "British-Indian",
			"birth_date": "1947-06-19",
		},
		{
			"author_name": "Chetan Bhagat",
			"biography": "Indian author, columnist, and screenwriter.",
			"nationality": "Indian",
			"birth_date": "1974-04-22",
		},
		{
			"author_name": "Ruskin Bond",
			"biography": "Indian author of British descent, known for his novels and short stories.",
			"nationality": "Indian",
			"birth_date": "1934-05-19",
		},
		{
			"author_name": "A.P.J. Abdul Kalam",
			"biography": "Indian aerospace scientist and 11th President of India.",
			"nationality": "Indian",
			"birth_date": "1931-10-15",
			"death_date": "2015-07-27",
		},
		{
			"author_name": "Sudha Murty",
			"biography": "Indian author, social worker, and chairperson of Infosys Foundation.",
			"nationality": "Indian",
			"birth_date": "1950-08-19",
		},
	]

	for author_data in authors:
		doc = frappe.new_doc("Author")
		for key, value in author_data.items():
			setattr(doc, key, value)
		doc.save()

	print(f"Created {len(authors)} authors")


def create_publishers():
	"""Create publisher records"""
	print("Creating Publishers...")

	publishers = [
		{
			"publisher_name": "Penguin Random House India",
			"address": "Noida, Uttar Pradesh, India",
			"contact_person": "Ravi Singh",
			"email": "info@penguinrandomhouse.co.in",
			"phone": "+91-120-4078900",
			"website": "https://penguinrandomhouse.co.in",
		},
		{
			"publisher_name": "HarperCollins India",
			"address": "New Delhi, India",
			"contact_person": "Ananth Padmanabhan",
			"email": "info@harpercollins.co.in",
			"phone": "+91-11-4174-7580",
			"website": "https://harpercollins.co.in",
		},
		{
			"publisher_name": "Oxford University Press India",
			"address": "New Delhi, India",
			"contact_person": "Sivaramakrishnan Venkateswaran",
			"email": "customercare.in@oup.com",
			"phone": "+91-11-4603-6100",
			"website": "https://india.oup.com",
		},
		{
			"publisher_name": "Rupa Publications",
			"address": "New Delhi, India",
			"contact_person": "Kapish Mehra",
			"email": "info@rupapublications.co.in",
			"phone": "+91-11-2327-6000",
			"website": "https://rupapublications.co.in",
		},
		{
			"publisher_name": "Westland Publications",
			"address": "Chennai, Tamil Nadu, India",
			"contact_person": "Gautam Padmanabhan",
			"email": "info@westlandbooks.in",
			"phone": "+91-44-4216-1616",
			"website": "https://westlandbooks.in",
		},
		{
			"publisher_name": "Hachette India",
			"address": "Gurugram, Haryana, India",
			"contact_person": "Thomas Abraham",
			"email": "info@hachetteindia.com",
			"phone": "+91-124-478-5600",
			"website": "https://hachetteindia.com",
		},
	]

	for pub_data in publishers:
		doc = frappe.new_doc("Publisher")
		for key, value in pub_data.items():
			setattr(doc, key, value)
		doc.save()

	print(f"Created {len(publishers)} publishers")


def create_book_categories():
	"""Create book category records"""
	print("Creating Book Categories...")

	categories = [
		{"category_name": "Fiction", "description": "Literary fiction, novels, and stories"},
		{"category_name": "Non-Fiction", "description": "Biographies, essays, and factual works"},
		{"category_name": "Science & Technology", "description": "Scientific and technical publications"},
		{"category_name": "History & Politics", "description": "Historical and political literature"},
		{"category_name": "Philosophy & Religion", "description": "Philosophical and religious texts"},
		{"category_name": "Children's Books", "description": "Books for children and young readers"},
		{"category_name": "Poetry & Drama", "description": "Poems, plays, and theatrical works"},
		{"category_name": "Reference", "description": "Dictionaries, encyclopedias, and reference materials"},
		{"category_name": "Regional Literature", "description": "Literature in regional Indian languages"},
		{"category_name": "Academic", "description": "Educational and academic textbooks"},
	]

	for cat_data in categories:
		doc = frappe.new_doc("Book Category")
		doc.category_name = cat_data["category_name"]
		doc.description = cat_data["description"]
		doc.save()

	print(f"Created {len(categories)} book categories")


def create_book_subcategories():
	"""Create book subcategory records"""
	print("Creating Book Subcategories...")

	subcategories = [
		{"subcategory_name": "Indian Fiction", "parent_category": "Fiction"},
		{"subcategory_name": "Contemporary Fiction", "parent_category": "Fiction"},
		{"subcategory_name": "Classic Literature", "parent_category": "Fiction"},
		{"subcategory_name": "Autobiographies", "parent_category": "Non-Fiction"},
		{"subcategory_name": "Business Books", "parent_category": "Non-Fiction"},
		{"subcategory_name": "Self-Help", "parent_category": "Non-Fiction"},
		{"subcategory_name": "Computer Science", "parent_category": "Science & Technology"},
		{"subcategory_name": "Physics & Mathematics", "parent_category": "Science & Technology"},
		{"subcategory_name": "Indian History", "parent_category": "History & Politics"},
		{"subcategory_name": "World History", "parent_category": "History & Politics"},
		{"subcategory_name": "Hinduism", "parent_category": "Philosophy & Religion"},
		{"subcategory_name": "Buddhism", "parent_category": "Philosophy & Religion"},
		{"subcategory_name": "Story Books", "parent_category": "Children's Books"},
		{"subcategory_name": "Educational Books", "parent_category": "Children's Books"},
		{"subcategory_name": "Hindi Poetry", "parent_category": "Poetry & Drama"},
		{"subcategory_name": "Bengali Literature", "parent_category": "Regional Literature"},
		{"subcategory_name": "Tamil Literature", "parent_category": "Regional Literature"},
	]

	for subcat_data in subcategories:
		doc = frappe.new_doc("Book Subcategory")
		doc.subcategory_name = subcat_data["subcategory_name"]
		doc.parent_category = subcat_data["parent_category"]
		doc.save()

	print(f"Created {len(subcategories)} book subcategories")


def create_library_locations():
	"""Create library location records"""
	print("Creating Library Locations...")

	locations = [
		{
			"location_name": "Ground Floor - Section A",
			"floor": "Ground Floor",
			"section": "A",
			"description": "Fiction and Literature",
		},
		{
			"location_name": "Ground Floor - Section B",
			"floor": "Ground Floor",
			"section": "B",
			"description": "Children's Books",
		},
		{
			"location_name": "First Floor - Section A",
			"floor": "First Floor",
			"section": "A",
			"description": "Science and Technology",
		},
		{
			"location_name": "First Floor - Section B",
			"floor": "First Floor",
			"section": "B",
			"description": "History and Politics",
		},
		{
			"location_name": "Second Floor - Section A",
			"floor": "Second Floor",
			"section": "A",
			"description": "Regional Literature",
		},
		{
			"location_name": "Second Floor - Section B",
			"floor": "Second Floor",
			"section": "B",
			"description": "Reference and Academic",
		},
		{
			"location_name": "Basement - Archives",
			"floor": "Basement",
			"section": "Archive",
			"description": "Rare and Old Books",
		},
	]

	for loc_data in locations:
		doc = frappe.new_doc("Library Location")
		for key, value in loc_data.items():
			setattr(doc, key, value)
		doc.save()

	print(f"Created {len(locations)} library locations")


def create_books():
	"""Create book records with authors"""
	print("Creating Books...")

	# Get actual names from database
	publishers = {doc.name: doc.name for doc in frappe.get_all("Publisher", fields=["name"])}
	languages = {doc.name: doc.name for doc in frappe.get_all("Language", fields=["name"])}
	categories = {doc.name: doc.name for doc in frappe.get_all("Book Category", fields=["name"])}
	subcategories = {doc.name: doc.name for doc in frappe.get_all("Book Subcategory", fields=["name"])}
	locations = {doc.name: doc.name for doc in frappe.get_all("Library Location", fields=["name"])}
	authors = {doc.name: doc.name for doc in frappe.get_all("Author", fields=["name"])}

	books_data = [
		{
			"isbn": "978-0143419326",
			"title": "Gitanjali",
			"subtitle": "A Collection of Poems",
			"authors": [("Rabindranath Tagore", "Primary")],
			"publisher": "Penguin Random House India",
			"publication_date": "2019-01-15",
			"edition": "Centenary Edition",
			"language": "English",
			"book_category": "Poetry & Drama",
			"subcategory": "Hindi Poetry",
			"tags": "poetry, nobel prize, spirituality",
			"description": "A collection of 103 English poems, originally translated from Bengali.",
			"total_copies": 5,
			"location": "Ground Floor - Section A",
			"rack_number": "A-001",
			"price": 299.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-8172234775",
			"title": "Malgudi Days",
			"subtitle": "",
			"authors": [("R.K. Narayan", "Primary")],
			"publisher": "Rupa Publications",
			"publication_date": "2018-03-10",
			"edition": "25th Edition",
			"language": "English",
			"book_category": "Fiction",
			"subcategory": "Indian Fiction",
			"tags": "short stories, malgudi, indian literature",
			"description": "A collection of short stories set in the fictional town of Malgudi.",
			"total_copies": 8,
			"location": "Ground Floor - Section A",
			"rack_number": "A-002",
			"price": 250.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-8171674213",
			"title": "Godan",
			"subtitle": "The Gift of a Cow",
			"authors": [("Premchand", "Primary")],
			"publisher": "Oxford University Press India",
			"publication_date": "2020-05-20",
			"edition": "Revised Edition",
			"language": "Hindi",
			"book_category": "Regional Literature",
			"subcategory": "Bengali Literature",
			"tags": "hindi literature, rural india, social issues",
			"description": "A classic Hindi novel depicting the life of a poor peasant.",
			"total_copies": 6,
			"location": "Second Floor - Section A",
			"rack_number": "SA-001",
			"price": 350.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-0143423416",
			"title": "A Suitable Boy",
			"subtitle": "",
			"authors": [("Vikram Seth", "Primary")],
			"publisher": "Penguin Random House India",
			"publication_date": "2017-11-15",
			"edition": "3rd Edition",
			"language": "English",
			"book_category": "Fiction",
			"subcategory": "Contemporary Fiction",
			"tags": "indian epic, post-independence, family saga",
			"description": "An epic novel set in post-Independence India.",
			"total_copies": 4,
			"location": "Ground Floor - Section A",
			"rack_number": "A-003",
			"price": 699.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-0006551225",
			"title": "The God of Small Things",
			"subtitle": "",
			"authors": [("Arundhati Roy", "Primary")],
			"publisher": "HarperCollins India",
			"publication_date": "2019-08-12",
			"edition": "Film Tie-in Edition",
			"language": "English",
			"book_category": "Fiction",
			"subcategory": "Contemporary Fiction",
			"tags": "booker prize, kerala, family drama",
			"description": "Booker Prize-winning novel set in Kerala.",
			"total_copies": 7,
			"location": "Ground Floor - Section A",
			"rack_number": "A-004",
			"price": 399.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-8129135728",
			"title": "Wings of Fire",
			"subtitle": "An Autobiography",
			"authors": [("A.P.J. Abdul Kalam", "Primary")],
			"publisher": "Rupa Publications",
			"publication_date": "2018-07-01",
			"edition": "10th Anniversary Edition",
			"language": "English",
			"book_category": "Non-Fiction",
			"subcategory": "Autobiographies",
			"tags": "autobiography, president, scientist",
			"description": "Autobiography of India's former President and scientist.",
			"total_copies": 10,
			"location": "First Floor - Section B",
			"rack_number": "FB-001",
			"price": 199.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-0143333623",
			"title": "Five Point Someone",
			"subtitle": "What Not to Do at IIT",
			"authors": [("Chetan Bhagat", "Primary")],
			"publisher": "Rupa Publications",
			"publication_date": "2020-02-14",
			"edition": "15th Anniversary Edition",
			"language": "English",
			"book_category": "Fiction",
			"subcategory": "Contemporary Fiction",
			"tags": "iit, engineering, youth fiction",
			"description": "A novel about three friends at IIT Delhi.",
			"total_copies": 12,
			"location": "Ground Floor - Section A",
			"rack_number": "A-005",
			"price": 150.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
		{
			"isbn": "978-0143330837",
			"title": "The Room on the Roof",
			"subtitle": "",
			"authors": [("Ruskin Bond", "Primary")],
			"publisher": "Penguin Random House India",
			"publication_date": "2019-04-10",
			"edition": "Special Edition",
			"language": "English",
			"book_category": "Fiction",
			"subcategory": "Indian Fiction",
			"tags": "coming of age, himalayas, youth",
			"description": "Coming-of-age story set in the hills of India.",
			"total_copies": 6,
			"location": "Ground Floor - Section B",
			"rack_number": "B-001",
			"price": 199.0,
			"acquisition_date": nowdate(),
			"condition": "New",
		},
	]

	for book_data in books_data:
		doc = frappe.new_doc("Book")

		# Set basic fields with validation
		for key, value in book_data.items():
			if key == "authors":
				continue
			elif key == "publisher" and value not in publishers:
				# Use first available publisher if specified one doesn't exist
				value = next(iter(publishers.keys())) if publishers else None
			elif key == "language" and value not in languages:
				value = next(iter(languages.keys())) if languages else None
			elif key == "book_category" and value not in categories:
				value = next(iter(categories.keys())) if categories else None
			elif key == "subcategory" and value not in subcategories:
				value = next(iter(subcategories.keys())) if subcategories else None
			elif key == "location" and value not in locations:
				value = next(iter(locations.keys())) if locations else None

			if value is not None:
				setattr(doc, key, value)

		# Add authors
		for author_name, author_type in book_data["authors"]:
			# Validate author exists
			validated_author = (
				author_name if author_name in authors else (next(iter(authors.keys())) if authors else None)
			)
			if validated_author:
				doc.append(
					"authors",
					{
						"author": validated_author,
						"author_type": author_type,
						"contribution_percentage": 100 if author_type == "Primary" else 50,
					},
				)

		doc.save()

	print(f"Created {len(books_data)} books")


def create_library_members():
	"""Create library member records"""
	print("Creating Library Members...")

	members_data = [
		{
			"member_type": "Student",
			"first_name": "Arjun",
			"last_name": "Sharma",
			"email": "arjun.sharma@email.com",
			"phone": "+91-9876543210",
			"address": "123 MG Road, New Delhi, Delhi 110001",
			"date_of_birth": "2000-05-15",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 12),
			"membership_status": "Active",
			"access_level": "Basic",
			"emergency_name": "Rajesh Sharma",
			"emergency_phone": "+91-9876543211",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "Fiction", "priority": "High"},
				{"preference_type": "Language", "preference_value": "English", "priority": "High"},
				{"preference_type": "Author", "preference_value": "R.K. Narayan", "priority": "Medium"},
			],
		},
		{
			"member_type": "Faculty",
			"first_name": "Priya",
			"last_name": "Patel",
			"email": "priya.patel@email.com",
			"phone": "+91-9876543212",
			"address": "456 Residency Road, Ahmedabad, Gujarat 380001",
			"date_of_birth": "1985-08-22",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 12),
			"membership_status": "Active",
			"max_books_allowed": 10,
			"access_level": "Premium",
			"emergency_name": "Kiran Patel",
			"emergency_phone": "+91-9876543213",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "Non-Fiction", "priority": "High"},
				{"preference_type": "Language", "preference_value": "English", "priority": "High"},
			],
		},
		{
			"member_type": "Student",
			"first_name": "Rohit",
			"last_name": "Kumar",
			"email": "rohit.kumar@email.com",
			"phone": "+91-9876543214",
			"address": "789 Park Street, Kolkata, West Bengal 700016",
			"date_of_birth": "1999-12-03",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 12),
			"membership_status": "Active",
			"access_level": "Basic",
			"emergency_name": "Sunita Kumar",
			"emergency_phone": "+91-9876543215",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "Science & Technology", "priority": "High"},
				{"preference_type": "Author", "preference_value": "A.P.J. Abdul Kalam", "priority": "High"},
			],
		},
		{
			"member_type": "Staff",
			"first_name": "Meera",
			"last_name": "Iyer",
			"email": "meera.iyer@email.com",
			"phone": "+91-9876543216",
			"address": "321 Mount Road, Chennai, Tamil Nadu 600002",
			"date_of_birth": "1990-03-18",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 12),
			"membership_status": "Active",
			"access_level": "Premium",
			"emergency_name": "Ravi Iyer",
			"emergency_phone": "+91-9876543217",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "Regional Literature", "priority": "High"},
				{"preference_type": "Language", "preference_value": "Tamil", "priority": "High"},
			],
		},
		{
			"member_type": "External",
			"first_name": "Vikram",
			"last_name": "Singh",
			"email": "vikram.singh@email.com",
			"phone": "+91-9876543218",
			"address": "654 Civil Lines, Jaipur, Rajasthan 302006",
			"date_of_birth": "1975-11-28",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 6),
			"membership_status": "Active",
			"max_books_allowed": 3,
			"access_level": "Basic",
			"emergency_name": "Anjali Singh",
			"emergency_phone": "+91-9876543219",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "History & Politics", "priority": "High"},
				{"preference_type": "Language", "preference_value": "Hindi", "priority": "Medium"},
			],
		},
		{
			"member_type": "Student",
			"first_name": "Ananya",
			"last_name": "Reddy",
			"email": "ananya.reddy@email.com",
			"phone": "+91-9876543220",
			"address": "987 Banjara Hills, Hyderabad, Telangana 500034",
			"date_of_birth": "2001-07-12",
			"membership_start_date": nowdate(),
			"membership_end_date": add_months(nowdate(), 12),
			"membership_status": "Active",
			"access_level": "Basic",
			"emergency_name": "Lakshmi Reddy",
			"emergency_phone": "+91-9876543221",
			"preferences": [
				{"preference_type": "Genre", "preference_value": "Fiction", "priority": "High"},
				{"preference_type": "Author", "preference_value": "Chetan Bhagat", "priority": "Medium"},
			],
		},
	]

	for member_data in members_data:
		doc = frappe.new_doc("Library Member")

		# Set basic fields
		preferences = member_data.pop("preferences", [])
		for key, value in member_data.items():
			setattr(doc, key, value)

		# Add preferences
		for pref in preferences:
			doc.append("preferences", pref)

		doc.save()

	print(f"Created {len(members_data)} library members")


def create_book_transactions():
	"""Create book transaction records"""
	print("Creating Book Transactions...")

	# Get some members and books for transactions
	members = frappe.get_all("Library Member", limit=6)
	books = frappe.get_all("Book", limit=10)

	if not members or not books:
		print("No members or books found for transactions")
		return

	transactions_data = [
		{
			"transaction_type": "Issue",
			"member": members[0]["name"],
			"book": books[0]["name"],
			"transaction_date": add_days(nowdate(), -10),
			"due_date": add_days(nowdate(), 4),
			"condition_on_issue": "Good",
		},
		{
			"transaction_type": "Issue",
			"member": members[1]["name"],
			"book": books[1]["name"],
			"transaction_date": add_days(nowdate(), -8),
			"due_date": add_days(nowdate(), 6),
			"condition_on_issue": "New",
		},
		{
			"transaction_type": "Issue",
			"member": members[2]["name"],
			"book": books[2]["name"],
			"transaction_date": add_days(nowdate(), -15),
			"due_date": add_days(nowdate(), -1),
			"condition_on_issue": "Good",
		},
		{
			"transaction_type": "Return",
			"member": members[3]["name"],
			"book": books[3]["name"],
			"transaction_date": add_days(nowdate(), -12),
			"due_date": add_days(nowdate(), -5),
			"return_date": add_days(nowdate(), -2),
			"condition_on_issue": "Good",
			"condition_on_return": "Good",
			"fine_amount": 6.0,
		},
		{
			"transaction_type": "Issue",
			"member": members[4]["name"],
			"book": books[4]["name"],
			"transaction_date": add_days(nowdate(), -5),
			"due_date": add_days(nowdate(), 9),
			"condition_on_issue": "New",
		},
		{
			"transaction_type": "Return",
			"member": members[5]["name"],
			"book": books[5]["name"],
			"transaction_date": add_days(nowdate(), -20),
			"due_date": add_days(nowdate(), -6),
			"return_date": nowdate(),
			"condition_on_issue": "Good",
			"condition_on_return": "Fair",
			"fine_amount": 12.0,
		},
	]

	for trans_data in transactions_data:
		doc = frappe.new_doc("Book Transaction")
		for key, value in trans_data.items():
			setattr(doc, key, value)

		doc.save()
		doc.submit()

	print("Created book transactions")


def create_fee_collections():
	"""Create fee collection records"""
	print("Creating Fee Collections...")

	# Get members with fines
	members_with_fines = frappe.db.sql(
		"""
        SELECT bt.member, SUM(bt.fine_amount) as total_fine
        FROM `tabBook Transaction` bt
        WHERE bt.docstatus = 1 AND bt.fine_amount > 0 AND bt.fine_paid = 0
        GROUP BY bt.member
        LIMIT 3
    """,
		as_dict=True,
	)

	if not members_with_fines:
		print("No members with fines found")
		return

	payment_methods = ["Cash", "Card", "UPI"]

	for i, member_fine in enumerate(members_with_fines):
		doc = frappe.new_doc("Fee Collection")
		doc.member = member_fine["member"]
		doc.payment_date = nowdate()
		doc.payment_type = "Fine Payment"
		doc.payment_method = payment_methods[i % len(payment_methods)]
		doc.fine_amount = member_fine["total_fine"]

		if doc.payment_method != "Cash":
			doc.reference_number = f"TXN{random.randint(100000, 999999)}"

		# Get fine details for this member
		fine_transactions = frappe.db.sql(
			"""
            SELECT name, book, fine_amount, transaction_date, due_date, return_date
            FROM `tabBook Transaction`
            WHERE member = %s AND docstatus = 1 AND fine_amount > 0 AND fine_paid = 0
        """,
			(member_fine["member"],),
			as_dict=True,
		)

		for fine_trans in fine_transactions:
			doc.append(
				"fine_details",
				{
					"transaction_id": fine_trans["name"],
					"book": fine_trans["book"],
					"fine_amount": fine_trans["fine_amount"],
					"transaction_date": fine_trans["transaction_date"],
					"due_date": fine_trans["due_date"],
					"return_date": fine_trans["return_date"],
				},
			)

		doc.save()
		doc.submit()

	print(f"Created {len(members_with_fines)} fee collections")
