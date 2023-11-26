from .sql_memory import build_memory
from .sql_window_memory import window_buffer_memory_builder
from functools import partial
memory_map = {
  "sql_buffer_memory":build_memory,
  "sql_window_buffer_memory_2":partial(window_buffer_memory_builder,k=2),
  "sql_window_buffer_memory_4":partial(window_buffer_memory_builder,k=2)
}