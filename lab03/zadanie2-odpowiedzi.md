1) Jaka jest różnica między `ENTRYPOINT` a `CMD`?

**Odpowiedź:**
CMD: Określa jakie argumenty zostaną przekazane do ENTRYPOINT (domyślne z dockerfile kiedy użytkownik ich nie podał).

ENTRYPOINT: Głowne polecenie uruchamiane po starcie kontenera. Domyślnie używane "/bin/sh -c". 

2) Jak każdą z powyższych opcji nadpisać podczas uruchamiania kontenera?

**Odpowiedź:**
CMD: Podajemy nowy argument
docker run container "Inna wiadomość"

ENTRYPOINT: Używamy flagi --entrypoint
docker run --entrypoint "/bin/sh" container

3) Jaka jest różnica między `ADD` a `COPY`?

**Odpowiedź:**
COPY: Kopiuje pliki z systemu hosta do kontenera.
COPY <src> <dest>

ADD: To samo co COPY ale dodatkowo obsługuje pobieranie plików z url oraz rozpakowuje archiwa .tar.
ADD <src> <dest>

4) Czy tylko jedno słowo kluczowe `FROM` może występować w pojedynczym pliku Dockerfile?

**Odpowiedź:**
Nie, można używać wiele FROM w jednym Dockerfile'u aby np. zbudować wiele obrazów równocześnie. 
Można użyć chociażby --target aby określić jaki odpalić wariant obrazu.
