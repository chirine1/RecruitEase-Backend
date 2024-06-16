1/ install python 3.12 + pipenv
2/pipenv install 
==> switch interpreter to venv 
3/pipenv shell
4/https://fastapi.tiangolo.com/async/  async await simple explanation
5/alembic migrations commands in /cmd.txt
delete old files in alembic/versions  then delete to migrate to a new clean database 
6/check .env 
7/ run with pipenv run python main.py  inside root directory 
8/ ignore this warning: 
 Argument of type "Column[int]" cannot be assigned to parameter "userId" of type "int | None" in function "__init__"
  Type "Column[int]" cannot be assigned to type "int | None"
    "Column[int]" is incompatible with "int"
    "Column[int]" is incompatible with "None"PylancereportArgumentType
(variable) id: Column[int]
this happens because of ide code is fine
9/ asaync i/o greenlet ==> we use session refresh 
10/ install gtk for weazyprint