# banco_de_horas

This project is a way to keep me track of the studies that I'm doing in my free time, and a way to make reports of how is it going. At the same time, it keeps me practising with personal projects and helps me develop my programming skills.

I'm doing it in my free time, and can be used for any kind of tracking, I'm focusing on study, but can be for habits, work, exercise. At first, I am doing everything by terminal, but at a second phase I'll use Streamlit to have a more approable face.

---


**Technologies**

- Docker
- Python (Pandas, SqlAlchemy)
- Postgresql


---

## How to run it down.

After installing the programs needed, maybe bash would be a good idead too, but just open a terminal and execute the `db_config.sh` script from the root of the repository:

```bash
src/db_config.sh
```

This script is the setup to create the database and to populate with the first themes, and study categories. It will pull a postgresql image do all the configuration needed in the container, and then it will exit.

This first script will run just one time, and it is for first configuration, after that execute a second script:
```bash
src/run_study_tracker.sh
```
