from sqlmodel import Field, SQLModel


class VersionHistory(SQLModel, table=True):
    __tablename__ = "version_history"
    id: int = Field(primary_key=True)
    tag: str = Field()
