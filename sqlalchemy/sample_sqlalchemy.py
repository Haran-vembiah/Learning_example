import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, UniqueConstraint, CheckConstraint, REAL, TEXT, FLOAT
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, INTEGER, ForeignKey, DefaultClause, Sequence, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

user = 'postgres'
password = '54321'
host = 'localhost'
port = '5432'
db = 'postgres'
schema = 'mgt'
schema_name = 'mgt'

url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
con = sqlalchemy.create_engine(url, client_encoding='utf8')


Session = sessionmaker(bind=con)
session = Session()

# meta = MetaData()
# meta.reflect(bind=con, schema=schema)
#
# print(meta)

Base = declarative_base()

class Requirement(Base):
    """
    This class is mapped to the requirement table in the Management schema.
    DB Comment: Mapping to TFS requirements. Since not all automated test cases may be found in TFS,
    traceability must be ensured internally.
    """
    __tablename__ = 'requirement'
    __table_args__ = {'schema': schema}

    req_id = Column(INTEGER(), primary_key=True, nullable=False)
    """Internal requirement ID."""
    title = Column(VARCHAR(length=2000), nullable=False)
    """Maps to TFS work item title."""
    tfs_link = Column(VARCHAR(length=2000))
    """Link to the work item in TFS."""
    tfs_id = Column(VARCHAR(length=250))
    """Maps to TFS ID."""
    mrd = Column(VARCHAR(length=250))
    """If the requirement is an SRD/TRD, this links it to the parent marketing requirement."""
    feature = Column(VARCHAR(length=2000))
    """Links the requirement to the parent feature. (Where applicable)"""
    req_type = Column(VARCHAR(length=10))
    """MRD, SRD, TRD or Backlog Item."""
    req_version = Column(REAL(precision=8, decimal_return_scale=8), primary_key=True, nullable=False,
                         server_default=DefaultClause("1.0", for_update=False))
    """The requirement version as it is stored in TFS, where applicable. Set to default for backlog items."""


class TcSuiteMap(Base):
    """
    This class is mapped to the tc_to_suite_map table in the Management schema.
    DB Comment: Define links between test suites and test cases in this table.
    """
    __tablename__ = 'tc_to_suite_map'
    __table_args__ = {'schema': schema_name}

    tc_id = Column(INTEGER(), ForeignKey(schema_name+'.'+'test_case.tc_id'), primary_key=True, nullable=False)
    tc_version = Column(REAL(), ForeignKey(schema_name+'.'+'test_case.tc_version'), primary_key=True, nullable=False)
    suite_id = Column(INTEGER(), ForeignKey(schema_name+'.'+'test_suite.suite_id'), primary_key=True, nullable=False)
    suite_version = Column(REAL(), ForeignKey(schema_name+'.'+'test_suite.suite_version'), primary_key=True, nullable=False)

    added_by = Column(VARCHAR())
    added_time = Column(TIMESTAMP())


class TestCase(Base):
    """
    This class is mapped to the test_case table in the Management schema.
    DB Comment: Can be an internal TAF test case or more likely a representation of a TFS test case.
    """
    __tablename__ = 'test_case'
    __table_args__ = {'schema': schema_name}

    tc_id_seq = Sequence('test_case_id_seq', metadata=Base.metadata)
    tc_id = Column(INTEGER(), Sequence('test_case_id_seq'), primary_key=True, nullable=False,
                   server_default=DefaultClause(tc_id_seq.next_value(), for_update=False))
    tc_title = Column(VARCHAR(length=500))
    """A short description of the test case."""
    tc_description = Column(TEXT())
    """The details of the test case, or even the test steps, if it is short or simple."""
    ext_id = Column(INTEGER())
    """A link to TFS if the TC represents a TFS entity."""
    tc_version = Column(REAL(), primary_key=True, nullable=False, server_default=DefaultClause('0.1', for_update=False))
    """The test case version. Each modification has to trigger a new version and a backup."""
    created_by = Column(VARCHAR(length=200), nullable=False)
    created_time = Column(TIMESTAMP(), nullable=False)
    last_modified_by = Column(VARCHAR(length=200))
    last_modified_time = Column(TIMESTAMP())
    # The database also has a CHECK constraint on this field for the allowed values: MANUAL, AUTO, BDD, DDT, KWD, COMBI
    # Here the CHECK constraint is passed as a string as SQLAlchemy doesn't know how to handle these, so this is
    # exactly as it appears in the PostgreSQL database
    # https://docs.sqlalchemy.org/en/13/core/constraints.html?highlight=constraint#check-constraint
    test_type = Column(VARCHAR(length=20), CheckConstraint("((test_type)::text = "
                                                           "ANY ((ARRAY['MANUAL'::character varying, "
                                                           "'AUTO'::character varying, "
                                                           "'BDD'::character varying, "
                                                           "'DDT'::character varying, "
                                                           "'KWD'::character varying])::text[]))"), nullable=False,
                       server_default=DefaultClause('AUTO', for_update=False))
    """MANUAL, AUTO, BDD, DDT, KWD, COMBI"""
    linked_test_id = Column(INTEGER())
    """The DB ID of a BDD feature or scenario, a KWD set a combinatorial set, or a TFS ID."""
    linked_test_format = Column(VARCHAR(length=20))
    """File, database, TFS."""


class TestSuite(Base):
    """
    This class is mapped to the test_suite table in the Management schema.
    DB Comment: Define test suites/sets in this table.
    """
    __tablename__ = 'test_suite'
    __table_args__ = {'schema': schema_name}

    suite_id = Column(INTEGER(), primary_key=True, nullable=False)
    suite_name = Column(VARCHAR(length=200), nullable=False)
    suite_description = Column(TEXT())
    suite_version = Column(REAL(), primary_key=True, nullable=False,
                           server_default=DefaultClause("0.1", for_update=False))
    created_by = Column(VARCHAR(length=200), nullable=False)
    created_time = Column(TIMESTAMP(), nullable=False)
    last_modified_by = Column(VARCHAR(length=200))
    last_modified_time = Column(TIMESTAMP())




for smap, tc, ts in session.query(TcSuiteMap, TestCase, TestSuite).\
        filter(TestCase.tc_id == TcSuiteMap.tc_id).\
        filter(TcSuiteMap.suite_id == TestSuite.suite_id).all():
    # print(smap.added_by)
    print(smap.added_time, tc.tc_title, ts.suite_name)

# for table in meta.sorted_tables:
#     print ("Table: ", table)
#     # print("Table code: ", table.__repr__())
#     for col in table.columns:
#         #print("\t", col.name, "\t", col.type, "\t", col.nullable, "\t", col.primary_key, "\t", col.foreign_keys)
#         print("\t", col.__repr__())
#
#
# for table in meta.sorted_tables:
#     print ("Table: ", table)

