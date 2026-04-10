import random
import string
from app.utils.validation import validate_abg_material_code


class MaterialCodeService:
    def __init__(self, exists_fn):
        self.exists_fn = exists_fn

    def _suffix(self) -> str:
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(4))

    def generate_unique(self, unspsc: str, max_attempts: int = 200) -> str:
        if len(unspsc) != 8 or not unspsc.isdigit():
            raise ValueError("UNSPSC must be exactly 8 digits")
        for _ in range(max_attempts):
            code = f"{unspsc}{self._suffix()}"
            validate_abg_material_code(code)
            if not self.exists_fn(code):
                return code
        raise RuntimeError("Could not generate unique ABG material code")
