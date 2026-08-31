from pathlib import Path
from collections import Counter


class DocumentMapper:

    def __init__(self, root: str | Path):

        self.root = Path(root).expanduser().resolve()

        if not self.root.exists():
            raise FileNotFoundError(
                f"Diretório não encontrado: {self.root}"
            )

        if not self.root.is_dir():
            raise NotADirectoryError(
                f"O caminho informado não é uma pasta: {self.root}"
            )

    def scan(self):

        mapping = {}

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            folder = file.parent.relative_to(self.root)

            extension = file.suffix.lower()

            if not extension:
                extension = "[SEM_EXTENSAO]"

            mapping.setdefault(folder, set())
            mapping[folder].add(extension)

        return mapping

    def generate_text(self):

        mapping = self.scan()

        lines = []

        root_name = self.root.name

        for folder in sorted(mapping, key=str):

            extensions = sorted(mapping[folder])

            formatted = []

            for extension in extensions:

                if extension == "[SEM_EXTENSAO]":

                    formatted.append(
                        "Arquivos.[SEM_EXTENSAO]"
                    )

                else:

                    formatted.append(
                        f"Arquivos.{extension.lstrip('.').upper()}"
                    )

            extension_text = ", ".join(formatted)

            if str(folder) == ".":

                path = root_name

            else:

                path = (
                    f"{root_name}/"
                    f"{str(folder).replace(chr(92), '/')}"
                )

            lines.append(
                f"{path}/[{extension_text}]"
            )

        return "\n".join(lines)

    def save(self, output: str | Path):

        output = Path(output).expanduser().resolve()

        output.write_text(
            self.generate_text(),
            encoding="utf-8"
        )

        return output

    def statistics(self):

        files = []
        directories = []

        for item in self.root.rglob("*"):

            if item.is_file():
                files.append(item)

            elif item.is_dir():
                directories.append(item)

        extensions = Counter()

        for file in files:

            extension = file.suffix.lower()

            if not extension:
                extension = "[SEM_EXTENSAO]"

            extensions[extension] += 1

        return {
            "root": str(self.root),
            "directories": len(directories),
            "files": len(files),
            "extensions": dict(
                sorted(extensions.items())
            )
        }