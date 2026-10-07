from .carguio.section import build_carguio_section
from .carguio_transporte.section import build_carguio_transporte_section
from .chancado_stmg.section import build_chancado_stmg_section
from src.features.dashboards.io.areas.flotacion.section import build_flotacion_section
from .general_mina.section import build_general_mina_section
from .molienda.section import build_molienda_section
from .puerto.section import build_puerto_section
from .stock_chacay.section.build import build_stock_chacay_section
from .transporte.section import build_transporte_section
from .transporte_fluidos.section import build_transporte_fluidos_section
from .header.section import build_header_section

__all__ = [
    'build_general_mina_section',
    'build_carguio_section',
    'build_carguio_transporte_section',
    'build_transporte_section',
    'build_chancado_stmg_section',
    'build_stock_chacay_section',
    'build_molienda_section',
    'build_flotacion_section',
    'build_transporte_fluidos_section',
    'build_puerto_section',
    'build_header_section'
]
