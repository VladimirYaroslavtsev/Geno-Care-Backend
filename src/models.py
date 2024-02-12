from pydantic import BaseModel


class Profile(BaseModel):
    name: str
    sex: str
    age: int


class Person(Profile):
    family_status: str
    medical_conditions: str


class FamilyTree(BaseModel):
    root: Person
    fammily: list[Person]


class Token(BaseModel):
    access_token: str
    token_type: str
