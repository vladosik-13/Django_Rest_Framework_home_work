import re
from django.core.exceptions import ValidationError


def youtube_url_validator(value):
    youtube_regex = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
    )
    if not youtube_regex.match(value):
        raise ValidationError(
            "Ссылка должна быть на YouTube (например, https://www.youtube.com/watch?v=example)."
        )
