from .areas.carguio.callbacks import register_carguio_callback
from .areas.carguio_transporte.callbacks import register_carguio_transporte_callback
from .areas.chancado_stmg.callbacks import register_chancado_stmg_callback
from .areas.general_mina.callbacks import register_general_mina_callback
from .areas.transporte.callbacks import register_transporte_callback
from .areas.header.callbacks import register_global_indicator_callback
from .areas.molienda.callbacks import register_molienda_callback
from .areas.flotacion.callbacks import register_flotacion_callback
from .areas.transporte_fluidos.callbacks import register_transporte_fluidos_callback
from .areas.puerto.callbacks import register_puerto_callback

def register_io_callback():
    register_transporte_callback()
    register_chancado_stmg_callback()
    register_carguio_transporte_callback()
    register_general_mina_callback()
    register_carguio_callback()
    register_global_indicator_callback()
    register_molienda_callback()
    register_flotacion_callback()
    register_transporte_fluidos_callback()
    register_puerto_callback()

__all__ = ['register_io_callback']
