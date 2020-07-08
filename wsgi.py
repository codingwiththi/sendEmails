#
# Conteudo do arquivo `wsgi.py`
#
import sys

sys.path.insert(0, "Users/thiag/PycharmProjects/sendEmails")

from enviaEmails import app as application