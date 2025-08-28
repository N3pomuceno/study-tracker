import os
import datetime
import pandas as pd
from requests import Session
from util.db_config import get_database_engine, load_environment_variables_for_db
from util.logger import setup_logger
from db_creation import Categoria, Materia, HorasEstudo

# from dbcreation import Materia, Categoria, HorasEstudo

logger = setup_logger()


def setup_engine():
    """
    Sets up the database engine using environment variables.
    """
    env_vars = load_environment_variables_for_db()
    return get_database_engine(env_vars)


def add_study_session(session_data: Session):
    # Get info necessary
    date = input("A data da sessão de estudo (YYYY-MM-DD): ")
    if not date:
        date = datetime.datetime.now()  # Default to current date
    else:
        # turn into datetime
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    horas = input("Número de horas estudadas (Formato de Float): ")
    # Get Materias disponíveis
    materias = session_data.query(Materia).all()
    for i, materia in enumerate(materias):
        print(f"{i + 1}. {materia.nome}")
    materia_id = input("Selecione a matéria estudada (número): ")
    materia_id = materias[int(materia_id) - 1].id
    # Get Categorias disponíveis
    categorias = session_data.query(Categoria).all()
    for i, categoria in enumerate(categorias):
        print(f"{i + 1}. {categoria.nome}")
    categoria_id = input("Selecione a categoria da sessão de estudo (número): ")
    categoria_id = categorias[int(categoria_id) - 1].id

    # Obter observações adicionais
    observacao = input("Observações adicionais (opcional): ")

    # Create a new study session
    new_study_session = HorasEstudo(
        data=date,
        horas=horas,
        materia_id=materia_id,
        categoria_id=categoria_id,
        observacao=observacao
    )
    session_data.add(new_study_session)
    session_data.commit()
    print("Sessão de estudo adicionada com sucesso!")


def view_recent_study_sessions(session_data: Session):
    """
        Considering recent study sessions in a interval of 15 days.
    """
    recent_sessions = (
        session_data.query(HorasEstudo, Materia, Categoria)
        .join(Materia, HorasEstudo.materia_id == Materia.id)
        .join(Categoria, HorasEstudo.categoria_id == Categoria.id)
        .order_by(HorasEstudo.data.desc())
        .where(HorasEstudo.data >= datetime.datetime.now() - datetime.timedelta(days=15))
        .all()
    )
    for horas_estudo, materia, categoria in recent_sessions:
        print(
            f"Data: {horas_estudo.data}, Horas: {horas_estudo.horas}, "
            f"Matéria: {materia.nome}, Categoria: {categoria.nome},",
            f"Observação: {horas_estudo.observacao if horas_estudo.observacao else 'Nenhuma'}"
        )


def edit_last_study_session(session_id, updated_data):
    # Code to edit the last study session in the database
    pass


def delete_last_study_session(session_id):
    # Code to delete the last study session from the database
    pass

def generate_weekly_report(session_data: Session):
    # Code to generate a weekly report
    pass

def generate_monthly_report(session_data: Session):
    # Code to generate a monthly report
    pass

def export_data(session_data: Session):
    data = session_data.query(HorasEstudo, Materia, Categoria) \
        .join(Materia, HorasEstudo.materia_id == Materia.id) \
        .join(Categoria, HorasEstudo.categoria_id == Categoria.id).all()
    df = pd.DataFrame([{
        'data': horas_estudo.data,
        'horas': horas_estudo.horas,
        'materia': materia.nome,
        'categoria': categoria.nome,
        'categoria_descricao': categoria.descricao,
        'observacao': horas_estudo.observacao
    } for horas_estudo, materia, categoria in data])
    df.to_csv("data/exported_data.csv", index=False)

def import_data(session_data: Session, file_path: str="data/imported_data.csv") -> None:

    if not os.path.exists(file_path):
        raise ValueError("File not found.")

    if not file_path.endswith('.csv'):
        raise ValueError("Only CSV files are supported for import.")
    
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        new_entry = HorasEstudo(
            data=row['data'],
            horas=row['horas'],
            materia_id=row['materia'],
            categoria_id=row['categoria'],
            observacao=row['observacao']
        )
        session_data.add(new_entry)
    session_data.commit()
