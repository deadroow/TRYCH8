import functools
from importlib import import_module

from... outils.Couleur import texte


class ROM:
    """Gère le chargement et la validation d'une ROM CHIP-8."""

    @staticmethod
    def check_path(fc):
        @functools.wraps(fc)
        def _(*args, **kwargs):
            if "path" in kwargs:
                os = import_module("os")
                if not os.path.exists(kwargs["path"]):
                    print(texte("Le chemin '{kwargs['path]}' n'existe pas.", "bleu"))
                    return
            return fc(*args, **kwargs)
        return _

    @staticmethod
    def check_rom_factory(checklist: list):
        def check_rom(fc):
            @functools.wraps(fc)
            def _(*args, **kwargs):
                for el in checklist:
                    if el == "len":
                        content   = kwargs.get("content", b"")
                        available = len(args[0].memory) - 0x200
                        if len(content) > available:
                            raise ValueError(
                                f"ROM trop volumineuse : {len(content)} bytes "
                                f"(max : {available} bytes)"
                            )
                return fc(*args, **kwargs)
            return _
        return check_rom

    @staticmethod
    def get_data_factory(mode="rb"):
        def get_data(fc):
            @functools.wraps(fc)
            def _(*args, **kwargs):
                if "path" in kwargs:
                    with open(kwargs["path"], mode=mode) as fp:
                        kwargs["content"] = fp.read()
                return fc(*args, **kwargs)
            return _
        return get_data


    @check_path
    @get_data_factory(mode="rb")
    @check_rom_factory(["len"])
    def load(self, *, path, content=None):
        """Copie la ROM en mémoire à partir de 0x200."""
        for i, byte in enumerate(content):
            self.memory[0x200 + i] = byte
        print(texte(f"ROM chargée ({len(content)} bytes) depuis '{path}'","vert"))
        return content
