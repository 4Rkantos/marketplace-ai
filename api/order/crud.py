from sqlalchemy.orm import Session
from models.order import Order, order_solutions
from models.solution import Solution
from models.order import OrderCreate

def create_order(db: Session, order: OrderCreate):
    # Criar o pedido
    db_order = Order(user_id=order.user_id, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Associar soluções ao pedido
    solutions = db.query(Solution).filter(Solution.id.in_(order.solution_ids)).all()
    db_order.solutions.extend(solutions)
    db.commit()

    # Retornar o pedido criado com os IDs das soluções
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "status": db_order.status,
        "solution_ids": [solution.id for solution in db_order.solutions]
    }


def get_order(db: Session, order_id: int):
    # Buscar o pedido com as soluções associadas
    db_order = db.query(Order).filter(Order.id == order_id).first()

    if db_order:
        # Obter os IDs das soluções associadas
        solution_ids = [solution.id for solution in db_order.solutions]
        return {
            "id": db_order.id,
            "user_id": db_order.user_id,
            "status": db_order.status,
            "solution_ids": solution_ids
        }
    return None


def get_orders_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    # Consultar pedidos do usuário com suas soluções associadas
    db_orders = db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    # Verifique se os pedidos estão sendo retornados
    if not db_orders:
        print(f"No orders found for user_id {user_id}")

    # Criar a resposta com os IDs das soluções para cada pedido
    orders_response = []
    for order in db_orders:
        solution_ids = [solution.id for solution in order.solutions]
        orders_response.append({
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "solution_ids": solution_ids
        })

    return orders_response


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    # Consultar todos os pedidos com suas soluções associadas
    db_orders = db.query(Order).offset(skip).limit(limit).all()

    # Criar a resposta com os IDs das soluções para cada pedido
    orders_response = []
    for order in db_orders:
        solution_ids = [solution.id for solution in order.solutions]
        orders_response.append({
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "solution_ids": solution_ids
        })

    return orders_response

