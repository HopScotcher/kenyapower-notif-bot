
```
kenya-power-notif-bot
├─ config
│  └─ settings.py
├─ data
│  └─ pdfs
│     ├─ 01JQBGP805M1M59157RSXTFR4W.pdf
│     ├─ 01JRJ9TXE0PNYESAQECD70S3YN.pdf
│     ├─ 01JWE3DAJTH2DBTJK6BZGEZDK9.pdf
│     └─ 2021(Revised)_Prepaid_Reallocation_&_Reversal.pdf
├─ main.py
├─ requirements.txt
└─ src
   ├─ notifications
   │  ├─ email_sender.py
   │  └─ __init__.py
   ├─ processors
   │  ├─ pdf_parser.py
   │  └─ __init__.py
   ├─ scrapers
   │  ├─ pdf_downloader.py
   │  └─ __init__.py
   └─ utils
      ├─ logger.py
      └─ __init__.py

```


#activate the virtual environment with the command below in terminal (run the command at the root of project)

env\Scripts\Activate.ps1

#deactivate the virtual env like so:

deactivate