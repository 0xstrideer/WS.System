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

        files = []

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            relative_path = file.relative_to(self.root)

            files.append(relative_path)

        return sorted(
            files,
            key=lambda path: str(path).lower()
        )

    def generate_text(self):

        files = self.scan()

        lines = []

        root_name = self.root.name

        for file in files:

            relative_path = str(file).replace("\\", "/")

            path = f"{root_name}/{relative_path}"

            lines.append(path)

        return "\n".join(lines)

    def save(self, output: str | Path | None = None):

        if output is None:

            downloads = Path.home() / "Downloads"

            output = downloads / "document_map.txt"

        else:

            output = Path(output).expanduser().resolve()

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

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