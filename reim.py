"""
Ein Programm mit dem man Reimwörter suchen kann
-
:author: chr3st5an
"""
from urllib.request import urlopen
from re import findall
from typing import List


class Reim(object):
    @classmethod
    def _get_html_code(cls, wort: str) -> str:
        try:
            response = urlopen(f'https://www.was-reimt-sich-auf.de/{wort}.html')
        except Exception:
            return ""
        return response.read().decode()
    
    @classmethod
    def suche(cls, wort: str, limit: int = None) -> List[str]:
        """Sucht nach Reimwörter des gesuchten Wortes

        Args:
            wort (str): Das Wort wonach Reime gesucht werden.
            limit (int, optional): Ein Limit, wie groß die
                die Liste mit gefundenen Reimwörtern sein
                darf. Wenn None, dann gibt es keine Grenze.

        Raises:
            Exception: Fehler beim Laden der Website.

        Returns:
            List[str]: Eine Liste mit gefundenen Reimwörtern.
        """
        if not isinstance(wort, str):
            raise ValueError("WARNUNG: Paramter 'wort' ist kein String!")
        if not isinstance(limit, int) and limit is not None:
            raise ValueError("WARNUNG: Paramter 'limit' ist kein Integer!")
        content = cls._get_html_code(wort.lower().replace("ß", "ss"))
        if limit is None:
            return findall(r'data-rhyme="(\w+(?#Reimwort))"', content)
        return findall(r'data-rhyme="(\w+(?#Reimwort))"', content)[:abs(limit)]
    
    def __init__(self, wort: str, limit: int = None) -> None:
        """Erstellt ein Reim Objekt

        Args:
            wort (str): Das Wort wonach Reime gesucht werden.
            limit (int, optional):  Ein Limit, wie groß die
                die Liste mit gefundenen Reimwörtern sein
                darf. Wenn None, dann gibt es keine Grenze.
                
        Examples:
            >>> for reim in Reim('Haus', limit=10):
            >>>     print(reim)
            >>> reim = Reim('Maus')
            >>> print(reim.reime)
            >>> print(reim[2])  # Äquivalent zu reim.reime[2]
            >>> print("maus" in reim) # True
            >>> reim.speicher()    
        """
        self.__wort = wort
        self.__wörter = self.suche(wort, limit=limit)
        
    def __repr__(self) -> str:
        return f'<Reim Objekt; gefunden={len(self)}; Reime={tuple(self[:5])}>'
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __len__(self) -> int:
        return len(self.__wörter)
    
    def __format__(self, _) -> str:
        if len(self.__wörter) < 2:
            return "-"
        return self[1]
    
    def __getitem__(self, pos: int) -> str:
        return self.__wörter[pos]
    
    def __contains__(self, wort: str) -> bool:
        return wort in self.__wörter
    
    def __iter__(self) -> iter:
        return iter(self.__wörter)
    
    @property
    def reime(self) -> List[str]:
        """Reimwörter die gefunden wurden

        Returns:
            List[str]: Eine Liste mit den Reimwörter
        """
        return self.__wörter
    
    def speicher(self, name: str = None, _max: int = None) -> None:
        """Erstellt eine *.txt Datei mit Reimwöter

        Args:
            name (str, optional): Der Name der Datei. Falls None,
                wird die Datei nach dem Wort benannt, wonach
                Reimwörter gesucht wurden. 
            _max (int, optional): Bestimmt, wie viele Wörter in 
                die Datei geschrieben werden. Falls None, werden
                alle Wörter in die Datei geschrieben.

        Raises:
            ValueError: _max ist kein Integer
        """
        name = str(name) if name is not None else self.__wort
        if not isinstance(_max, int) and _max is not None:
            raise ValueError("WARNUNG: Paramter 'limit' ist kein Integer!")
        with open(f'{name}.txt', 'w') as f:
            f.write("\n".join(self[:len(self) if not _max else abs(_max)]))
            

if __name__ == '__main__':
    from typing import NoReturn
    import sys
    
    
    class CommandLine(object):
        commands: List[str] = ['--help', '-h', '--all', '-a']
        
        def __init__(self, args: List[str]) -> NoReturn:
            if not len(args):
                print("Erhalte hilfe mit --help")
            elif args[0] in self.commands[:2]:
                self._help()
            elif len(args) == 1 or args[1] not in self.commands[2:]:
                print(Reim(args[0]))
            else:
                print(Reim(args[0]).reime)
            sys.exit(0)
        
        def _help(self) -> None:
            text = """
                \rHilfe
                \r----------------------------------------------
                \rBenutzung: < Wort | -h | --help > [-a | --all]
                \r----------------------------------------------
                \r
                \rArgs
                \r----------------------------------------------
                \rWort:
                \rDas Wort wonach Reime gesucht werden soll.\n
                \rHilfe (-h | --help):
                \rZeigt Hilfe an. Wer häts gedacht?\n
                \rAlles (-a | --all):
                \rZeigt alle gefundenen Reimwörter an. 
                \r
                \rAuthor
                \r----------------------------------------------
                \r@chr3st5an
            """
            return print(text)
    
    CommandLine(sys.argv[1:])
