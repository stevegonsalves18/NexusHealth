"""
Pydantic schemas package.
"""
from .auth import LoginRequest, RegisterRequest, Token, UserOut  # noqa: F401
from .prediction import PredictionRequest, PredictionResponse  # noqa: F401
from .records import ChatLogCreate  # noqa: F401
from .appointments import *  # noqa: F401,F403
from .clinical import *  # noqa: F401,F403
from .pharmacy import *  # noqa: F401,F403
from .discharge import *  # noqa: F401,F403
from .hospital import *  # noqa: F401,F403
from .nursing import *  # noqa: F401,F403
