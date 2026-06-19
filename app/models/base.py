"""
=============================================================
  OOP Concept: ABSTRACTION & INHERITANCE (Base Model)
=============================================================
  - Abstraction: We define WHAT every model should do
    (find, create, update, delete) without saying HOW.
  - Inheritance: Child classes (like User) will inherit
    these methods and reuse them automatically.
  - Encapsulation: The database connection details are
    hidden inside this class — outside code never sees them.
=============================================================
"""

from abc import ABC, abstractmethod
from .database import Database


class BaseModel(ABC):
    """
    Abstract Base Class for all models.

    ABC = Abstract Base Class
    - You CANNOT create an object of BaseModel directly.
    - Child classes MUST define the 'table' property.
    - Child classes INHERIT all the helper methods below.
    """

    # ── Abstract Property (child MUST define this) ──────────
    @property
    @abstractmethod
    def table(self):
        """Each child model must specify its database table name."""
        pass

    # ── Shared Methods (inherited by all child models) ──────

    # @abstractmethod
    # def save(self):
    #     pass

    def find_by_id(self, record_id):
        """Find a single record by its ID."""
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE id = %s", (record_id,)
        )
        db.close()
        return result

 