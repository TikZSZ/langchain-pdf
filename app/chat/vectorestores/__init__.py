from functools import partial
from .pincone import build_retriver

retriever_map = {
  "pincone_1":partial(build_retriver,k=1),
  "pincone_2":partial(build_retriver,k=2),
  "pincone_3":partial(build_retriver,k=3),
}