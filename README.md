### Library Management

Advanced Library Management Platform

### Training Tasks

This repository includes training materials to help you understand Frappe development concepts through practical implementation.

#### Task 1: Create DocTypes Based on Entity Relationships

**Objective**: Create all the necessary DocTypes for the Library Management system based on the defined entity relationships.

**Description**: Using the detailed entity relationship diagram and specifications provided in the documentation, you will create DocTypes that form the foundation of the library management system. This includes master data entities (Authors, Books, Members), configuration entities (Settings, Library Hours), and transaction entities (Book Transactions, Fee Collections).

**Learning Outcomes**:
- Understand DocType creation in Frappe
- Learn about field types and their relationships
- Implement parent-child relationships
- Configure naming series and auto-generated fields
- Set up calculated fields and validation rules

**Reference Documentation**: [DocType Relationships & Data Flow](library_management/docs/01_doctype_relationships.md)

**Getting Started**:
1. Review the entity relationship diagram in the documentation
2. Start with master entities (Author, Publisher, Language, BookCategory)
3. Move on to main entities (Book, LibraryMember)
4. Implement child tables (BookAuthor, MemberPreferences)
5. Create transaction DocTypes (BookTransaction, FeeCollection)
6. Add configuration DocTypes (LibrarySettings, LibraryHours)

