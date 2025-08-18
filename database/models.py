import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, Enum as SQLAlchemyEnum, func, \
    create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from config.settings import settings

con_str = settings.DATABASE_URL
Engine = create_engine(con_str, echo=True, pool_size=100)
Base = declarative_base()

Session = sessionmaker(bind=Engine)


class OrderStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    PURCHASE = "purchase"
    REFUND = "refund"


class TransactionStatus(enum.Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    balance = Column(Numeric(10, 2), default=0.0, nullable=False)
    purchases = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=True)

    orders = relationship("Order", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(String(100), nullable=True)
    order_data = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, status={self.status.value})>"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(SQLAlchemyEnum(TransactionType), nullable=False)
    status = Column(SQLAlchemyEnum(TransactionStatus), default=TransactionStatus.COMPLETED)
    payment_method = Column(String(100), nullable=True)
    transaction_data = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.transaction_type.value})>"

def create_tables():
    Base.metadata.create_all(Engine)


def drop_tables():
    Base.metadata.drop_all(Engine)