import datetime as datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String, Column, DateTime, func
from typing import List, Optional
from sqlalchemy.types import Boolean, DateTime
from sqlalchemy.schema import Table



from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    created_at = Column(DateTime, default=func.now())


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_category_id: Mapped[Optional[int]]
    name: Mapped[str]
    url: Mapped[Optional[str]]
    img_url: Mapped[Optional[str]]

    products: Mapped[Optional[List["Product"]]] = relationship(back_populates="category")
    meta_upgrade_id: Mapped[int] = mapped_column(ForeignKey("meta_upgrade.id"))
    meta_upgrade: Mapped["Meta_Upgrade"] = relationship("Meta_Upgrade", back_populates="categories")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    price: Mapped[Optional[int]]
    url: Mapped[Optional[str]]
    img_url: Mapped[Optional[str]]

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    meta_upgrade_id: Mapped[int] = mapped_column(ForeignKey("meta_upgrade.id"))
    meta_upgrade: Mapped["Meta_Upgrade"] = relationship("Meta_Upgrade", back_populates="products")




class Meta_Upgrade(Base):
    __tablename__ = "meta_upgrade"
    id: Mapped[int] = mapped_column(primary_key=True)

    products: Mapped[Optional[List["Product"]]] = relationship(back_populates="meta_upgrade")
    categories: Mapped[Optional[List["Category"]]] = relationship(back_populates="meta_upgrade")

association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("users_groups.id")),
)

orderproduct = Table(
    "OrderProduct_table",
    Base.metadata,
    Column("products_id", ForeignKey("products.id")),
    Column("order_id", ForeignKey("orders.id")),
)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]  # добавляем поле telegram_id
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    language_code: Mapped[Optional[str]]
    geo_position: Mapped[Optional[str]]

    groups: Mapped[List["User_group"]] = relationship(secondary=association_table)
    messages: Mapped[Optional[List["Message"]]] = relationship(back_populates="user")
    orders: Mapped[Optional[List["Order"]]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"id={self.id!r}, telegram_id={self.telegram_id!r}, username={self.username!r})"


# группы пользователей
class User_group(Base):
    __tablename__ = 'users_groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str]

    def __repr__(self) -> str:
        return f"group_name = {self.group_name!r})"


# Заказ пользователей"""
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[Optional[str]]
    status: Mapped[Optional[str]]
    products: Mapped[List["Product"]] = relationship(secondary=orderproduct)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="orders")



class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime.datetime]
    text: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="messages")
