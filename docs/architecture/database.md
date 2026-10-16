# Database Architecture — Recall Talk

This document outlines the relational database schema of the application, which combines spaced repetition tracking via the **FSRS algorithm (`py-fsrs`)** with AI-driven interactive conversation sessions and performance evaluations.

---

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    users ||--o{ speaking_sessions : "has"
    users ||--o{ review_cards : "owns"
    users ||--o{ learning_items : "creates (optional)"
    learning_items ||--o{ review_cards : "tracks"
    speaking_sessions ||--o{ practice_attempts : "contains"
    learning_items ||--o{ practice_attempts : "practiced in (0..1)"
    review_cards ||--o{ practice_attempts : "updates (0..1)"

    users {
        uuid id PK
        varchar(100) name
        varchar(255) email UK
        varchar(10) native_language
        varchar(10) target_language
        varchar(2) proficiency_level
        timestamptz created_at
        boolean is_active
    }

    learning_items {
        uuid id PK
        varchar(200) content
        varchar(200) normalized_content
        text meaning
        varchar(20) item_type
        varchar(10) target_language
        varchar(10) native_language
        text example_sentences
        varchar(2) proficiency_level
        varchar(20) visibility
        varchar(20) source
        uuid created_by_user_id FK "nullable"
        timestamptz created_at
    }

    review_cards {
        uuid id PK
        uuid user_id FK
        uuid learning_item_id FK
        bigint fsrs_card_id
        varchar(20) state
        integer step
        float stability
        float difficulty
        timestamptz due
        timestamptz last_review
        timestamptz created_at
        timestamptz updated_at
    }

    speaking_sessions {
        uuid id PK
        uuid user_id FK
        varchar(20) status
        timestamptz started_at
        timestamptz ended_at
        timestamptz created_at
    }

    practice_attempts {
        uuid id PK
        uuid speaking_session_id FK
        uuid learning_item_id FK "nullable"
        uuid review_card_id FK "nullable"
        varchar(20) mode
        text prompt
        text user_response
        text feedback
        text correction
        float score
        boolean was_successful
        timestamptz created_at
    }
```

> **Note:** A static rendering of this diagram is also available at [`database_diagram.png`](./database_diagram.png).

---

## 2. Design Decisions & Data Integrity

1. **Flexibility in `practice_attempts`**:
   - `learning_item_id` and `review_card_id` are optional (`NULLABLE`). This design allows a practice attempt to represent either a **targeted practice session** (bound to specific pre-existing vocabulary/grammar and an FSRS review card) or an unconstrained **free conversation** interaction (where the user practices dialogue with the AI without a registered learning item).
2. **Normalization in `practice_attempts`**:
   - There is no direct `user_id` foreign key on `practice_attempts`. Every attempt strictly belongs to a `speaking_session`, which in turn belongs to a `user`. This avoids redundant data and prevents data anomalies where an attempt could reference a user different from the session owner.
3. **FSRS Deck Integrity (`review_cards`)**:
   - `UNIQUE (user_id, learning_item_id)`: Prevents a user from having duplicate review cards tracking the exact same learning content.
   - `UNIQUE (user_id, fsrs_card_id)`: The `fsrs_card_id` (generated as a millisecond epoch timestamp by `py-fsrs`) is scoped uniquely per user, preventing collisions in concurrent multi-user environments.
4. **Content Storage (`learning_items`)**:
   - The `example_sentences` field is stored as a `TEXT` column, providing lightweight storage and broad compatibility across database engines.

---

## 3. Enums Dictionary

| Enum | Allowed Values | Description |
|---|---|---|
| `ProficiencyLevel` | `A1`, `A2`, `B1`, `B2`, `C1`, `C2` | Common European Framework of Reference for Languages (CEFR) levels. |
| `ItemType` | `WORD`, `EXPRESSION`, `GRAMMAR` | Category of the linguistic item being studied. |
| `LearningItemVisibility` | `PERSONAL`, `SHARED` | Indicates whether the item is private to the creator or shared globally. |
| `LearningItemSource` | `USER_CREATED`, `AGENT_SUGGESTED` | Content origin (manually registered by a user or suggested by an AI agent). |
| `SpeakingSessionStatus` | `ACTIVE`, `COMPLETED`, `ABANDONED` | Lifecycle status of a user's speaking practice session. |
| `PracticeMode` | `TARGETED`, `FREE_CONVERSATION` | Mode of the attempt (focused practice vs. free conversation). |
| `FSRSState` | `Learning`, `Review`, `Relearning` | Memory state of the card managed by the FSRS algorithm. |
