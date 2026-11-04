

# TV Show Catalog ERD

This is my ERD for a TV show catalog.

## Assumptions

- A show has a title, a release year, and a number of episodes.
- A show can have more than one genre.
- A show can have no actors, especially documentaries.
- One person can be both an actor and a writer.
- A show may not have a rating yet.
- Each show can have at most one overall rating.

## ERD

```mermaid
erDiagram
    SHOWS ||--o{ GENRES : has
    SHOWS ||--o{ STARS : has
    PEOPLE ||--o{ STARS : appears_in
    SHOWS ||--o{ WRITERS : has
    PEOPLE ||--o{ WRITERS : writes
    SHOWS ||--o| RATINGS : has

    SHOWS {
        int id PK
        string title
        int year
        int episodes
    }

    PEOPLE {
        int id PK
        string name
        int birth
    }

    GENRES {
        int show_id PK,FK
        string genre PK
    }

    STARS {
        int show_id PK,FK
        int person_id PK,FK
    }

    WRITERS {
        int show_id PK,FK
        int person_id PK,FK
    }

    RATINGS {
        int show_id PK,FK
        float rating
        int votes
    }
```
