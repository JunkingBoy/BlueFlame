from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:test@localhost/bf')
Session = sessionmaker(bind=engine)

session = Session()



try:
    # 假设你有一个主表 MainTable 和两个附表 SubTable1 和 SubTable2
    main = MainTable(name='main')
    session.add(main)
    session.flush()  # flush 会立即执行 SQL，这样我们就可以获取 main 的 id

    sub1 = SubTable1(name='sub1', p_id=main.id)
    sub2 = SubTable2(name='sub2', p_id=main.id)
    session.add(sub1)
    session.add(sub2)

    session.commit()
except Exception as e:
    session.rollback()
    print(f"Error inserting data: {e}")
finally:
    session.close()
