"""Single source of truth for natural-language, read-only SQL queries."""

from typing import Any

from app.models import (
    Author,
    Book,
    BookGenre,
    BookStatus,
    BookTag,
    Chapter,
    Genre,
    Review,
    Tag,
)

ColumnMetadata = dict[str, Any]
TableMetadata = dict[str, Any]
JoinStep = tuple[type, Any]


def column(
    sql_column: Any,
    data_type: str,
    description: str,
    *aliases: str,
) -> ColumnMetadata:
    """Describe one allowed column and retain its SQLAlchemy expression."""
    metadata: ColumnMetadata = {
        "column": sql_column,
        "type": data_type,
        "description": description,
    }
    if aliases:
        metadata["aliases"] = list(aliases)
    return metadata


TABLES: dict[str, TableMetadata] = {
    "book": {
        "model": Book,
        "description": "A novel published on the platform.",
        "aliases": ["book", "novel", "story", "truyện", "sách"],
        "columns": {
            "id": column(Book.id, "integer", "Unique book identifier."),
            "author_id": column(Book.author_id, "uuid", "Identifier of the author."),
            "name": column(Book.name, "string", "Book title.", "title", "tên truyện"),
            "slug": column(Book.slug, "string", "URL-friendly unique book name."),
            "kind": column(Book.kind, "integer", "Book kind code."),
            "sex": column(Book.sex, "integer", "Target audience gender code."),
            "status_id": column(Book.status_id, "integer", "Identifier of the book status."),
            "chapter_per_week": column(
                Book.chapter_per_week, "integer", "Expected chapters per week."
            ),
            "published": column(
                Book.published, "boolean", "Whether the book is publicly visible."
            ),
            "poster": column(
                Book.poster,
                "object",
                "Book cover and banner image variants used by the client.",
                "cover",
                "banner",
                "ảnh bìa",
            ),
            "synopsis": column(Book.synopsis, "string", "Short summary of the book."),
            "view_count": column(
                Book.view_count, "integer", "Cumulative book views.", "views", "lượt xem"
            ),
            "chapter_count": column(Book.chapter_count, "integer", "Number of chapters."),
            "word_count": column(Book.word_count, "integer", "Total word count."),
            "comment_count": column(Book.comment_count, "integer", "Number of comments."),
            "review_count": column(Book.review_count, "integer", "Number of reviews."),
            "average_rating": column(
                Book.average_rating, "number", "Average reader rating."
            ),
            "bookmark_count": column(
                Book.bookmark_count, "integer", "Number of bookmarks."
            ),
            "new_chap_at": column(
                Book.new_chap_at, "datetime", "Time of the latest chapter update."
            ),
            "created_at": column(Book.created_at, "datetime", "Book creation time."),
            "updated_at": column(Book.updated_at, "datetime", "Last book update time."),
            "published_at": column(Book.published_at, "datetime", "Book publication time."),
        },
    },
    "author": {
        "model": Author,
        "description": "An author associated with one or more books.",
        "aliases": ["author", "tác giả"],
        "columns": {
            "id": column(Author.id, "uuid", "Unique author identifier."),
            "name": column(Author.name, "string", "Author name."),
            "local_name": column(Author.local_name, "string", "Localized author name."),
            "created_at": column(Author.created_at, "datetime", "Author creation time."),
            "updated_at": column(Author.updated_at, "datetime", "Last author update time."),
        },
    },
    "book_status": {
        "model": BookStatus,
        "description": "Publication state of a book, such as ongoing or completed.",
        "aliases": ["status", "trạng thái"],
        "columns": {
            "id": column(BookStatus.id, "integer", "Unique status identifier."),
            "name": column(BookStatus.name, "string", "Human-readable status name."),
            "slug": column(BookStatus.slug, "string", "Stable status code."),
            "description": column(
                BookStatus.description, "string", "Explanation of the status."
            ),
        },
    },
    "genre": {
        "model": Genre,
        "description": "A genre assigned to books.",
        "aliases": ["genre", "thể loại"],
        "columns": {
            "id": column(Genre.id, "integer", "Unique genre identifier."),
            "name": column(Genre.name, "string", "Genre name."),
            "slug": column(Genre.slug, "string", "Stable genre code."),
            "description": column(Genre.description, "string", "Genre explanation."),
        },
    },
    "tag": {
        "model": Tag,
        "description": "A tag used to categorize books.",
        "aliases": ["tag", "nhãn"],
        "columns": {
            "id": column(Tag.id, "integer", "Unique tag identifier."),
            "name": column(Tag.name, "string", "Tag name."),
            "slug": column(Tag.slug, "string", "Stable tag code."),
            "type": column(Tag.type, "string", "Tag category."),
            "description": column(Tag.description, "string", "Tag explanation."),
        },
    },
    "chapter": {
        "model": Chapter,
        "description": "Metadata for a chapter belonging to a book.",
        "aliases": ["chapter", "chương"],
        "columns": {
            "id": column(Chapter.id, "integer", "Unique chapter identifier."),
            "book_id": column(Chapter.book_id, "integer", "Identifier of the parent book."),
            "name": column(Chapter.name, "string", "Chapter title."),
            "index": column(Chapter.index, "integer", "Chapter number within the book."),
            "word_count": column(Chapter.word_count, "integer", "Chapter word count."),
            "view_count": column(Chapter.view_count, "integer", "Cumulative chapter views."),
            "comment_count": column(
                Chapter.comment_count, "integer", "Number of chapter comments."
            ),
            "published": column(
                Chapter.published, "boolean", "Whether the chapter is publicly visible."
            ),
            "created_at": column(Chapter.created_at, "datetime", "Chapter creation time."),
            "updated_at": column(Chapter.updated_at, "datetime", "Last chapter update time."),
            "published_at": column(
                Chapter.published_at, "datetime", "Chapter publication time."
            ),
        },
    },
    "review": {
        "model": Review,
        "description": "A numeric rating submitted for a book.",
        "aliases": ["review", "rating", "đánh giá"],
        "columns": {
            "id": column(Review.id, "uuid", "Unique review identifier."),
            "book_id": column(Review.book_id, "integer", "Identifier of the reviewed book."),
            "rating": column(Review.rating, "integer", "Numeric rating."),
            "created_at": column(Review.created_at, "datetime", "Review creation time."),
            "updated_at": column(Review.updated_at, "datetime", "Last review update time."),
        },
    },
}

# Each relationship has a stable ID that the LLM may select.
RELATIONSHIPS: dict[str, dict[str, Any]] = {
    "book.author": {
        "source": "book", "target": "author",
        "description": "The author who wrote the book.",
        "steps": [(Author, Book.author_id == Author.id)],
    },
    "author.books": {
        "source": "author", "target": "book",
        "description": "Books written by the author.",
        "steps": [(Book, Book.author_id == Author.id)],
    },
    "book.status": {
        "source": "book", "target": "book_status",
        "description": "The current status of the book.",
        "steps": [(BookStatus, Book.status_id == BookStatus.id)],
    },
    "book_status.books": {
        "source": "book_status", "target": "book",
        "description": "Books having this status.",
        "steps": [(Book, Book.status_id == BookStatus.id)],
    },
    "book.chapters": {
        "source": "book", "target": "chapter",
        "description": "Chapters belonging to the book.",
        "steps": [(Chapter, Chapter.book_id == Book.id)],
    },
    "chapter.book": {
        "source": "chapter", "target": "book",
        "description": "The book containing the chapter.",
        "steps": [(Book, Chapter.book_id == Book.id)],
    },
    "book.reviews": {
        "source": "book", "target": "review",
        "description": "Ratings submitted for the book.",
        "steps": [(Review, Review.book_id == Book.id)],
    },
    "review.book": {
        "source": "review", "target": "book",
        "description": "The book associated with the rating.",
        "steps": [(Book, Review.book_id == Book.id)],
    },
    "book.genres": {
        "source": "book", "target": "genre",
        "description": "Genres assigned to the book.",
        "steps": [
            (BookGenre, BookGenre.book_id == Book.id),
            (Genre, Genre.id == BookGenre.genre_id),
        ],
    },
    "genre.books": {
        "source": "genre", "target": "book",
        "description": "Books assigned to the genre.",
        "steps": [
            (BookGenre, BookGenre.genre_id == Genre.id),
            (Book, Book.id == BookGenre.book_id),
        ],
    },
    "book.tags": {
        "source": "book", "target": "tag",
        "description": "Tags assigned to the book.",
        "steps": [
            (BookTag, BookTag.book_id == Book.id),
            (Tag, Tag.id == BookTag.tag_id),
        ],
    },
    "tag.books": {
        "source": "tag", "target": "book",
        "description": "Books assigned to the tag.",
        "steps": [
            (BookTag, BookTag.tag_id == Tag.id),
            (Book, Book.id == BookTag.book_id),
        ],
    },
}

DEFAULT_FILTERS = {
    "book": [(Book.published, "=", True)],
    "chapter": [(Chapter.published, "=", True)],
}

HIDDEN_TABLES = {"user", "chapter_content", "comment", "refresh_token"}

RULES = [
    "Only SELECT queries are allowed.",
    "Never expose credentials, user emails, tokens, comments, or chapter content.",
    "Use COUNT(DISTINCT book.id) when counting books after a genre or tag join.",
    "Historical views are unsupported because only cumulative counts are stored.",
]

QUERY_CATALOG: dict[str, Any] = {
    "version": 4,
    "tables": TABLES,
    "relationships": RELATIONSHIPS,
    "default_filters": DEFAULT_FILTERS,
    "hidden_tables": HIDDEN_TABLES,
    "rules": RULES,
}


def get_table(table_name: str) -> TableMetadata:
    """Return metadata for an approved table."""
    if table_name in HIDDEN_TABLES or table_name not in TABLES:
        raise KeyError(f"Table is unavailable for natural-language queries: {table_name}")
    return TABLES[table_name]


def get_table_name(field_name: str) -> str:
    """Return the table name from a fully qualified field."""
    table_name, separator, _ = field_name.partition(".")
    if not separator:
        raise ValueError(f"Field must include its table name: {field_name}")
    return table_name


def get_model(table_name: str) -> type:
    """Return the SQLModel class for an approved table."""
    return get_table(table_name)["model"]


def get_column(field_name: str) -> Any:
    """Resolve a fully qualified field to its SQLAlchemy column."""
    table_name, separator, column_name = field_name.partition(".")
    if not separator:
        raise KeyError(f"Field must include its table name: {field_name}")
    try:
        return get_table(table_name)["columns"][column_name]["column"]
    except KeyError as error:
        raise KeyError(f"Field is unavailable: {field_name}") from error



def get_table_name(field_name: str) -> str:
    """Return the table name from a fully qualified field."""
    table_name, separator, _ = field_name.partition(".")
    if not separator:
        raise ValueError(f"Field must include its table name: {field_name}")
    return table_name



def is_allowed_field(field_name: str) -> bool:
    """Return whether a fully qualified field is exposed by the catalog."""
    try:
        get_column(field_name)
    except KeyError:
        return False
    return True


def get_relationship(relationship_id: str) -> dict[str, Any] | None:
    """Return an approved relationship by its stable ID."""
    return RELATIONSHIPS.get(relationship_id)


def has_direct_relationship(source_table: str, target_table: str) -> bool:
    """Return whether the catalog can access target from source."""
    if source_table == target_table:
        return True
    return any(
        relationship["source"] == source_table
        and relationship["target"] == target_table
        for relationship in RELATIONSHIPS.values()
    )


def build_llm_catalog() -> dict[str, Any]:
    """Build a serializable catalog without Python models or SQL expressions."""
    tables: dict[str, Any] = {}
    for table_name, table in TABLES.items():
        tables[table_name] = {
            "description": table["description"],
            "aliases": table.get("aliases", []),
            "columns": {
                column_name: {
                    key: value
                    for key, value in metadata.items()
                    if key != "column"
                }
                for column_name, metadata in table["columns"].items()
            },
        }

    relationships = {
        relationship_id: {
            "source": relationship["source"],
            "target": relationship["target"],
            "description": relationship["description"],
        }
        for relationship_id, relationship in RELATIONSHIPS.items()
    }

    return {
        "version": QUERY_CATALOG["version"],
        "tables": tables,
        "relationships": relationships,
        "rules": RULES,
    }

