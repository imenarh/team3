# MoMo SMS data processing system

## Team 3

**Names of team members**
    - Ganza Gavin
    - Isingizwe Benito
    - Herve IMENA Rwigema
    - Orla Ishimwe

## Project Description

Throughout this term, we will be working on a tool that processes MTN MoMo SMS transaction data taken from XML, categorizes and stores it in a relational database, and presents the data through a web dashboard.


## Database Design

The Application database schema has these entities:

- **user:** unique `phone_number` (STANDARD, MERCHANT, or AGENT).
- **transaction:** core event: `reference_id`, amount, fee, status, `raw_sms_text`, `timestamp`.
- **transaction_category:** types such as P2P transfer, airtime, merchant payment, cash in/out.
- **user_transactions:** junction table linking users to transactions with `role` (SENDER or RECEIVER) and optional `balance_after` from the SMS.
- **system_logs:** Application activity logs (INFO, WARNING, ERROR), which can, optionally, be tied to a transaction.


## Important Links

- [Scrum Board](https://github.com/users/imenarh/projects/3)
- [Architecture Diagram](https://miro.com/app/board/uXjVHX2Nt5w=/?share_link_id=716970547823)
- [Entity Relations Diagram](https://lucid.app/lucidchart/f356b840-4e66-4cea-adf7-85052defeea7/view)


## Week 2 — Database Design & Implementation

- The SQL setup script ([database/database_setup.sql](database/database_setup.sql))
- The JSON schema file ([examples/json_schemas.json](examples/json_schemas.json))
- CRUD & Constraint testing script ([database/crud_tests.sql](database/crud_tests.sql)) 

### Deliverables

- [ERD Diagram](https://lucid.app/lucidchart/f356b840-4e66-4cea-adf7-85052defeea7/view) | [Local copy](docs/erd_diagram.png)
- [Database Design Documentation (PDF)](docs/team3-database_design-documentation.pdf)
- [Team Participation Sheet](https://docs.google.com/spreadsheets/d/1WZS6NH4f0jmcaSMB3EdFt1luvqu5WgidfMUH905gTS4/edit?usp=sharing)
- [Scrum Board](https://github.com/users/imenarh/projects/3)
