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
- Set up workspace for users

**Reference Documentation**: [DocType Relationships & Data Flow](library_management/docs/01_doctype_relationships.md)

**Getting Started**:
1. Review the entity relationship diagram in the documentation
2. Start with master entities (Author, Publisher, Language, BookCategory)
3. Move on to main entities (Book, LibraryMember)
4. Implement child tables (BookAuthor, MemberPreferences)
5. Create transaction DocTypes (BookTransaction, FeeCollection)
6. Add configuration DocTypes (LibrarySettings, LibraryHours)

#### Task 2: Implement Book Issue Process Validations

**Objective**: Create server-side validations and business logic for the Book Issue process based on the defined process flow.

**Learning Outcomes**:
- Understand Frappe validation hooks and lifecycle methods
- Implement server-side business logic validation
- Create custom validation messages and error handling
- Work with linked DocTypes and fetch related data
- Use Frappe's database query methods

**Reference Documentation**: [Process Flows & Business Logic](library_management/docs/02_process_flows.md)

**Validation Requirements**:
1. **Member Validation**: Verify member exists and has active membership status
2. **Book Availability**: Check if book is available and not reference-only
3. **Issue Limit Check**: Ensure member hasn't exceeded maximum books allowed
4. **Outstanding Fines**: Block issue if member has unpaid fines
5. **Duplicate Issue Prevention**: Prevent issuing same book to same member twice
6. **Due Date Calculation**: Auto-set due date based on library settings
7. **Inventory Updates**: Automatically update book's available_copies count

**Getting Started**:
1. Review the Book Issue Process Flow diagram
2. Create validation methods in BookTransaction DocType
3. Implement before_insert and before_submit hooks
4. Add custom validation messages for each business rule
5. Test validation scenarios with different member/book combinations

