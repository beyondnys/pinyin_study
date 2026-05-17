You are required to generate MySQL table DDL following STRICT rules below. Do not deviate.

[GENERAL RULES]
1. Every table MUST include standard audit fields:
   - enabled_flag
   - created_at
   - creation_date
   - updated_at
   - updation_date
   - is_deleted

2. Every column MUST have a COMMENT in English explaining its meaning.

3. Table MUST use:
   - ENGINE=InnoDB
   - DEFAULT CHARSET=utf8mb4
   - COLLATE=utf8mb4_unicode_ci

4. All column names MUST use snake_case.

5. Avoid NULL unless absolutely necessary. Prefer NOT NULL with default values.

6. Every table MUST have a primary key:
   - id BIGINT UNSIGNED AUTO_INCREMENT

7. Every table MUST include at least:
   - one UNIQUE constraint (business key)
   - necessary secondary indexes

8. All datetime fields MUST use:
   - DATETIME type
   - CURRENT_TIMESTAMP as default when applicable

9. Do NOT use FLOAT or DOUBLE for financial values. Use:
   - DECIMAL(18,2)

10. All status/type fields MUST define explicit semantic meaning in COMMENT.

---

[AUDIT FIELDS – MANDATORY EXACT STRUCTURE]

Include EXACTLY the following fields:

enabled_flag TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Enable flag: 1 enabled, 0 disabled',

created_at VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'Created by',
creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',

updated_at VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'Updated by',
updation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update time',

is_deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Delete flag: 0 not deleted, 1 deleted'

---

[NAMING CONVENTIONS]

1. Primary key: id
2. Name field: name
3. Code field: code
4. Description: description
5. Sort field: sort_order
6. Status field: status (must define meaning)

Forbidden variations:
- create_time, update_time, gmt_create, etc.

---

[INDEX RULES]

1. MUST include:
   PRIMARY KEY (id)

2. MUST include indexes:
   - creation_date
   - enabled_flag
   - is_deleted

3. MUST define at least one UNIQUE index (e.g., code)

---

[OPTIONAL ADVANCED FIELDS – include if applicable]

tenant_id BIGINT DEFAULT 0 COMMENT 'Tenant ID',
version INT DEFAULT 1 COMMENT 'Version for optimistic locking'

---

[OUTPUT REQUIREMENTS]

1. Output ONLY valid MySQL CREATE TABLE statement
2. Do NOT include explanations
3. Do NOT omit any required fields
4. Ensure formatting is clean and production-ready

---

[QUALITY STANDARD]

The generated schema must be:
- Auditable (who + when)
- Controllable (enable/disable + soft delete)
- Consistent (strict naming + typing)
- Performant (proper indexing)
- Maintainable (clear comments)