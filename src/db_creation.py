from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from util.db_config import get_database_engine, load_environment_variables_for_db, setup_engine
from util.logger import setup_logger

logger = setup_logger(level="INFO")


# --- Definição dos Modelos ORM ---

# Base class for our models
Base = declarative_base()


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String)

    # This defines the "many" side of the one-to-many relationship
    # It links back to the 'categoria' attribute in HorasEstudo
    horas_estudo = relationship("HorasEstudo", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(nome='{self.nome}')>"


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    # This defines the "many" side of the one-to-many relationship
    # It links back to the 'materia' attribute in HorasEstudo
    horas_estudo = relationship("HorasEstudo", back_populates="materia")

    def __repr__(self):
        return f"<Materia(nome='{self.nome}')>"


class HorasEstudo(Base):
    __tablename__ = "horas_estudo"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False, default=datetime.now())
    horas = Column(Float, nullable=False)
    observacao = Column(String)

    # These columns hold the ID of the related Categoria and Materia
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # These attributes create the link to the actual Python objects
    materia = relationship("Materia", back_populates="horas_estudo")
    categoria = relationship("Categoria", back_populates="horas_estudo")

    def __repr__(self):
        return f"<HorasEstudo(data='{self.data}', horas='{self.horas}', materia='{self.materia.nome}')>"


# --- Função para Criar e Popular o Banco de Dados ---


def setup_database(engine) -> None:
    """
    Creates all database tables and populates initial data for categories and subjects.
    This function is idempotent, meaning it can be run multiple times without creating duplicates.
    """
    logger.info("Iniciando setup do banco de dados...")

    # Create all tables defined by Base's subclasses
    Base.metadata.create_all(engine)
    logger.info("Tabelas verificadas/criadas com sucesso.")

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # --- Dados Iniciais ---
        categorias_iniciais = [
            {
                "nome": "TEORIA_LEITURA",
                "descricao": "Estudo de teoria através de PDFs, livros e apostilas.",
            },
            {
                "nome": "TEORIA_VIDEO",
                "descricao": "Estudo de teoria através de vídeo-aulas.",
            },
            {
                "nome": "QUESTOES_TOPICO",
                "descricao": "Resolução de questões focadas em um tópico específico.",
            },
            {
                "nome": "SIMULADO_PROVA",
                "descricao": "Realização de provas antigas ou simulados completos.",
            },
            {
                "nome": "REVISAO_FLASHCARD",
                "descricao": "Revisão ativa utilizando sistema de repetição espaçada (Anki).",
            },
            {
                "nome": "REVISAO_RESUMO",
                "descricao": "Revisão de resumos, mapas mentais e anotações.",
            },
            {
                "nome": "ANALISE_ERROS",
                "descricao": "Análise detalhada de questões erradas.",
            },
        ]

        materias_iniciais = [
            {"nome": "Direito Administrativo"},
            {"nome": "Direito Constitucional"},
            {"nome": "Matemática"},
            {"nome": "Português"},
            {"nome": "Estatística"},
            {"nome": "Ciência de Dados"},
            {"nome": "Políticas Públicas"},
            # {'nome': 'Outra'} # Good to have a fallback
        ]

        # --- Lógica "Create if not exists" ---
        logger.info("Verificando e inserindo categorias iniciais...")
        for cat_data in categorias_iniciais:
            existe = session.query(Categoria).filter_by(nome=cat_data["nome"]).first()
            if not existe:
                nova_categoria = Categoria(
                    nome=cat_data["nome"], descricao=cat_data["descricao"]
                )
                session.add(nova_categoria)
                logger.info(f"  - Categoria '{cat_data['nome']}' adicionada.")

        logger.info("Verificando e inserindo matérias iniciais...")
        for mat_data in materias_iniciais:
            existe = session.query(Materia).filter_by(nome=mat_data["nome"]).first()
            if not existe:
                nova_materia = Materia(nome=mat_data["nome"])
                session.add(nova_materia)
                logger.info(f"  - Matéria '{mat_data['nome']}' adicionada.")

        # Commit all changes to the database
        session.commit()
        logger.info("Dados iniciais populados com sucesso.")

    except Exception as e:
        logger.info(f"Ocorreu um erro durante o setup: {e}")
        session.rollback()
    finally:
        session.close()


# --- Execução Principal ---
if __name__ == "__main__":
    # 1. Carregar variáveis de ambiente, Criar a engine do banco de dados
    engine = setup_engine()

    # 2. Rodar a função de setup
    setup_database(engine)

    logger.info(
        "\nSetup concluído. O banco de dados 'study_tracker.db' está pronto para uso."
    )
