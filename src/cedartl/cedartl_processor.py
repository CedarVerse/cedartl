import re
from importlib.resources.abc import Traversable
from typing import Match


class CedarTLProcessor:
    _file_pattern = r'[a-zA-Z/:]+[a-zA-Z0-9.:/-]*[a-zA-Z0-9]'
    _special_pattern = r'[$*]\([^)]+\)'
    template_regex = re.compile(
        r'([^\\]?)\\' 
        f'({_file_pattern}|{_special_pattern})'
    )

    def __init__(self, main_template_folder: Traversable, proj_root: Traversable):
        self.root = proj_root
        self.main_template_folder = main_template_folder
        self._processing_stack: set[str] = set()

    def load_template(self, template_name: str) -> str:
        """Load template file contents.

        Args:
            template_name: Name of the template file without extension

        Returns:
            Template content or original template command if loading fails
        """
        try:
            template_path = self.main_template_folder / f"{template_name}.cedartl"
            return template_path.read_text()
        except (OSError, IOError) as e:
            # Log error here
            return f"\\{template_name}"

    def process(self, text: str | None) -> str | None:
        """Process text and replace template patterns.

        Args:
            text: Input text containing template patterns

        Returns:
            Processed text with replaced templates or None if input is None
        """
        if not text:
            return text

        def replace_template(match: Match) -> str:
            prev, template_name = match.groups()
            if template_name in self._processing_stack:
                return f"{prev}\\{template_name}"  # Break recursion by returning original command

            self._processing_stack.add(template_name)
            template_content = self.load_template(template_name)
            if f"\\{template_name}" != template_content:
                print(f'[CedarTL] \\{template_name}: {template_content.strip()}')
            result = self.process(prev + template_content)
            self._processing_stack.remove(template_name)
            return result

        return self.template_regex.sub(replace_template, text)
